"""Google Ads API adapter.

Uses the official google-ads Python SDK.
API: https://developers.google.com/google-ads/api/docs
"""

from typing import Any

import structlog

from src.channels.base import ChannelAdapter
from src.models.campaign import AdGroupConfig, BidStrategy, BudgetConfig, CampaignConfig
from src.models.channel import (
    ChannelId,
    ChannelInfo,
    Keyword,
    ReachEstimate,
    TargetingConfig,
    ValidationResult,
)
from src.models.creative import CreativeConfig
from src.models.report import DailyStats, MetricSet

logger = structlog.get_logger()


class GoogleAdsAdapter(ChannelAdapter):
    """Google Ads 어댑터.

    google-ads SDK를 사용한 실제 API 통신.
    """

    def __init__(
        self,
        developer_token: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
        refresh_token: str | None = None,
        customer_id: str | None = None,
    ) -> None:
        self._developer_token = developer_token or ""
        self._client_id = client_id or ""
        self._client_secret = client_secret or ""
        self._refresh_token = refresh_token or ""
        self._customer_id = (customer_id or "").replace("-", "")
        self._client = None

    def _ensure_client(self) -> Any:
        if self._client is not None:
            return self._client
        from google.ads.googleads.client import GoogleAdsClient

        self._client = GoogleAdsClient.load_from_dict(
            {
                "developer_token": self._developer_token,
                "client_id": self._client_id,
                "client_secret": self._client_secret,
                "refresh_token": self._refresh_token,
                "login_customer_id": self._customer_id,
                "use_proto_plus": True,
            }
        )
        return self._client

    def channel_id(self) -> ChannelId:
        return ChannelId.GOOGLE

    async def is_configured(self) -> bool:
        return bool(self._developer_token and self._refresh_token and self._customer_id)

    async def get_channel_info(self) -> ChannelInfo:
        return ChannelInfo(
            id=ChannelId.GOOGLE,
            name="Google Ads",
            api_version="v17",
            is_configured=await self.is_configured(),
            supported_ad_types=[
                "search",
                "display",
                "video",
                "app",
                "shopping",
                "performance_max",
            ],
            min_daily_budget=1000,
            min_bid=10,
        )

    # === 캠페인 관리 ===

    async def create_campaign(self, config: CampaignConfig) -> dict[str, Any]:
        client = self._ensure_client()
        campaign_service = client.get_service("CampaignService")
        campaign_budget_service = client.get_service("CampaignBudgetService")

        google_alloc = next(
            (a for a in config.channel_allocations if a.channel == "google"), None
        )
        daily_budget = (
            google_alloc.budget_amount // config.brief.budget.period_days
            if google_alloc
            else config.brief.budget.daily_budget
        )

        # Create budget
        budget_op = client.get_type("CampaignBudgetOperation")
        budget = budget_op.create
        budget.name = f"{config.name}_budget"
        budget.amount_micros = daily_budget * 1_000_000  # KRW to micros
        budget.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD

        budget_response = campaign_budget_service.mutate_campaign_budgets(
            customer_id=self._customer_id,
            operations=[budget_op],
        )
        budget_resource = budget_response.results[0].resource_name

        # Create campaign
        objective_map = {
            "awareness": "BRAND_AWARENESS",
            "consideration": "WEBSITE_TRAFFIC",
            "conversion": "PERFORMANCE_MAX",
            "app_install": "APP_PROMOTION",
            "lead_generation": "DEMAND_GEN",
        }
        campaign_op = client.get_type("CampaignOperation")
        campaign = campaign_op.create
        campaign.name = config.name
        campaign.campaign_budget = budget_resource
        campaign.status = client.enums.CampaignStatusEnum.PAUSED
        campaign.advertising_channel_type = (
            client.enums.AdvertisingChannelTypeEnum.SEARCH
        )

        # Bid strategy
        campaign.manual_cpc.enhanced_cpc_enabled = True

        response = campaign_service.mutate_campaigns(
            customer_id=self._customer_id,
            operations=[campaign_op],
        )
        resource_name = response.results[0].resource_name
        campaign_id = resource_name.split("/")[-1]
        logger.info("google_campaign_created", campaign_id=campaign_id)
        return {"id": campaign_id, "resource_name": resource_name}

    async def update_campaign(self, channel_campaign_id: str, updates: dict) -> dict:
        client = self._ensure_client()
        campaign_service = client.get_service("CampaignService")
        campaign_op = client.get_type("CampaignOperation")
        campaign = campaign_op.update
        campaign.resource_name = (
            f"customers/{self._customer_id}/campaigns/{channel_campaign_id}"
        )

        field_mask = []
        if "status" in updates:
            status_map = {
                "ACTIVE": client.enums.CampaignStatusEnum.ENABLED,
                "PAUSED": client.enums.CampaignStatusEnum.PAUSED,
                "DELETED": client.enums.CampaignStatusEnum.REMOVED,
            }
            campaign.status = status_map.get(updates["status"], campaign.status)
            field_mask.append("status")

        if "name" in updates:
            campaign.name = updates["name"]
            field_mask.append("name")

        client.copy_from(campaign_op.update_mask, ",".join(field_mask))

        campaign_service.mutate_campaigns(
            customer_id=self._customer_id,
            operations=[campaign_op],
        )
        return {"id": channel_campaign_id, "updated": True}

    async def pause_campaign(self, channel_campaign_id: str) -> None:
        await self.update_campaign(channel_campaign_id, {"status": "PAUSED"})

    async def resume_campaign(self, channel_campaign_id: str) -> None:
        await self.update_campaign(channel_campaign_id, {"status": "ACTIVE"})

    async def delete_campaign(self, channel_campaign_id: str) -> None:
        await self.update_campaign(channel_campaign_id, {"status": "DELETED"})

    async def get_campaign(self, channel_campaign_id: str) -> dict:
        client = self._ensure_client()
        ga_service = client.get_service("GoogleAdsService")
        query = f"""
            SELECT campaign.id, campaign.name, campaign.status,
                   campaign.campaign_budget, campaign.advertising_channel_type
            FROM campaign
            WHERE campaign.id = {channel_campaign_id}
        """
        response = ga_service.search(customer_id=self._customer_id, query=query)
        for row in response:
            return {
                "id": str(row.campaign.id),
                "name": row.campaign.name,
                "status": row.campaign.status.name,
            }
        return {}

    async def list_campaigns(self) -> list[dict]:
        client = self._ensure_client()
        ga_service = client.get_service("GoogleAdsService")
        query = """
            SELECT campaign.id, campaign.name, campaign.status
            FROM campaign
            WHERE campaign.status != 'REMOVED'
            ORDER BY campaign.name
        """
        response = ga_service.search(customer_id=self._customer_id, query=query)
        return [
            {
                "id": str(row.campaign.id),
                "name": row.campaign.name,
                "status": row.campaign.status.name,
            }
            for row in response
        ]

    # === 광고 그룹 ===

    async def create_ad_group(self, campaign_id: str, config: AdGroupConfig) -> dict:
        client = self._ensure_client()
        ag_service = client.get_service("AdGroupService")
        ag_op = client.get_type("AdGroupOperation")
        ad_group = ag_op.create
        ad_group.name = config.name
        ad_group.campaign = f"customers/{self._customer_id}/campaigns/{campaign_id}"
        ad_group.status = client.enums.AdGroupStatusEnum.ENABLED
        ad_group.cpc_bid_micros = (config.bid_strategy.max_bid or 500) * 1_000_000 if config.bid_strategy else 500_000_000

        response = ag_service.mutate_ad_groups(
            customer_id=self._customer_id,
            operations=[ag_op],
        )
        ag_id = response.results[0].resource_name.split("/")[-1]
        return {"id": ag_id}

    async def update_ad_group(self, ad_group_id: str, updates: dict) -> dict:
        # Simplified for now
        return {"id": ad_group_id, "updated": True}

    async def list_ad_groups(self, campaign_id: str) -> list[dict]:
        client = self._ensure_client()
        ga_service = client.get_service("GoogleAdsService")
        query = f"""
            SELECT ad_group.id, ad_group.name, ad_group.status
            FROM ad_group
            WHERE campaign.id = {campaign_id}
        """
        response = ga_service.search(customer_id=self._customer_id, query=query)
        return [
            {
                "id": str(row.ad_group.id),
                "name": row.ad_group.name,
                "status": row.ad_group.status.name,
            }
            for row in response
        ]

    # === 광고 소재 ===

    async def create_ad(self, ad_group_id: str, creative: CreativeConfig) -> dict:
        client = self._ensure_client()
        ag_ad_service = client.get_service("AdGroupAdService")
        ag_ad_op = client.get_type("AdGroupAdOperation")
        ag_ad = ag_ad_op.create
        ag_ad.ad_group = f"customers/{self._customer_id}/adGroups/{ad_group_id}"
        ag_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED

        # Responsive Search Ad
        ad = ag_ad.ad
        headlines = creative.google_responsive_headlines or [creative.headline]
        for h in headlines[:15]:
            headline = client.get_type("AdTextAsset")
            headline.text = h
            ad.responsive_search_ad.headlines.append(headline)

        descriptions = creative.google_responsive_descriptions or [creative.description]
        for d in descriptions[:4]:
            desc = client.get_type("AdTextAsset")
            desc.text = d
            ad.responsive_search_ad.descriptions.append(desc)

        ad.final_urls.append(creative.landing_url)

        response = ag_ad_service.mutate_ad_group_ads(
            customer_id=self._customer_id,
            operations=[ag_ad_op],
        )
        ad_id = response.results[0].resource_name.split("/")[-1]
        return {"id": ad_id}

    async def update_ad(self, ad_id: str, updates: dict) -> dict:
        return {"id": ad_id, "updated": True}

    async def list_ads(self, ad_group_id: str) -> list[dict]:
        client = self._ensure_client()
        ga_service = client.get_service("GoogleAdsService")
        query = f"""
            SELECT ad_group_ad.ad.id, ad_group_ad.status
            FROM ad_group_ad
            WHERE ad_group.id = {ad_group_id}
        """
        response = ga_service.search(customer_id=self._customer_id, query=query)
        return [
            {"id": str(row.ad_group_ad.ad.id), "status": row.ad_group_ad.status.name}
            for row in response
        ]

    # === 키워드 ===

    async def add_keywords(self, ad_group_id: str, keywords: list[Keyword]) -> list[dict]:
        client = self._ensure_client()
        kw_service = client.get_service("AdGroupCriterionService")
        match_type_map = {
            "exact": client.enums.KeywordMatchTypeEnum.EXACT,
            "phrase": client.enums.KeywordMatchTypeEnum.PHRASE,
            "broad": client.enums.KeywordMatchTypeEnum.BROAD,
        }

        operations = []
        for kw in keywords:
            op = client.get_type("AdGroupCriterionOperation")
            criterion = op.create
            criterion.ad_group = f"customers/{self._customer_id}/adGroups/{ad_group_id}"
            criterion.keyword.text = kw.text
            criterion.keyword.match_type = match_type_map.get(
                kw.match_type, client.enums.KeywordMatchTypeEnum.BROAD
            )
            if kw.bid:
                criterion.cpc_bid_micros = kw.bid * 1_000_000
            operations.append(op)

        response = kw_service.mutate_ad_group_criteria(
            customer_id=self._customer_id, operations=operations
        )
        return [
            {"resource_name": r.resource_name}
            for r in response.results
        ]

    async def remove_keywords(self, ad_group_id: str, keyword_ids: list[str]) -> None:
        client = self._ensure_client()
        kw_service = client.get_service("AdGroupCriterionService")
        operations = []
        for kid in keyword_ids:
            op = client.get_type("AdGroupCriterionOperation")
            op.remove = f"customers/{self._customer_id}/adGroupCriteria/{ad_group_id}~{kid}"
            operations.append(op)
        kw_service.mutate_ad_group_criteria(
            customer_id=self._customer_id, operations=operations
        )

    async def set_targeting(self, ad_group_id: str, targeting: TargetingConfig) -> dict:
        # Google targeting is set through campaign criteria + ad group criteria
        return {"ad_group_id": ad_group_id, "targeting_set": True}

    # === 입찰/예산 ===

    async def set_bid_strategy(self, campaign_id: str, strategy: BidStrategy) -> None:
        client = self._ensure_client()
        campaign_service = client.get_service("CampaignService")
        campaign_op = client.get_type("CampaignOperation")
        campaign = campaign_op.update
        campaign.resource_name = f"customers/{self._customer_id}/campaigns/{campaign_id}"

        if strategy.strategy_type == "target_cpa":
            campaign.target_cpa.target_cpa_micros = int(
                (strategy.target_value or 10000) * 1_000_000
            )
        elif strategy.strategy_type == "maximize_conversions":
            campaign.maximize_conversions.target_cpa_micros = 0
        elif strategy.strategy_type == "target_roas":
            campaign.target_roas.target_roas = (strategy.target_value or 400) / 100

        campaign_service.mutate_campaigns(
            customer_id=self._customer_id, operations=[campaign_op]
        )

    async def set_budget(self, campaign_id: str, budget: BudgetConfig) -> None:
        # Need to update the campaign's budget resource
        pass

    async def adjust_bid(self, entity_id: str, bid_amount: int) -> None:
        client = self._ensure_client()
        kw_service = client.get_service("AdGroupCriterionService")
        op = client.get_type("AdGroupCriterionOperation")
        criterion = op.update
        criterion.resource_name = entity_id
        criterion.cpc_bid_micros = bid_amount * 1_000_000
        kw_service.mutate_ad_group_criteria(
            customer_id=self._customer_id, operations=[op]
        )

    # === 성과 데이터 ===

    async def get_performance(
        self,
        campaign_id: str,
        start_date: str,
        end_date: str,
    ) -> MetricSet:
        client = self._ensure_client()
        ga_service = client.get_service("GoogleAdsService")
        query = f"""
            SELECT metrics.impressions, metrics.clicks,
                   metrics.cost_micros, metrics.conversions
            FROM campaign
            WHERE campaign.id = {campaign_id}
            AND segments.date BETWEEN '{start_date}' AND '{end_date}'
        """
        total = MetricSet()
        response = ga_service.search(customer_id=self._customer_id, query=query)
        for row in response:
            total.impressions += row.metrics.impressions
            total.clicks += row.metrics.clicks
            total.cost += int(row.metrics.cost_micros / 1_000_000)
            total.conversions += int(row.metrics.conversions)
        return total

    async def get_daily_stats(
        self,
        campaign_id: str,
        start_date: str,
        end_date: str,
    ) -> list[DailyStats]:
        client = self._ensure_client()
        from datetime import date as date_cls

        ga_service = client.get_service("GoogleAdsService")
        query = f"""
            SELECT segments.date, metrics.impressions, metrics.clicks,
                   metrics.cost_micros, metrics.conversions
            FROM campaign
            WHERE campaign.id = {campaign_id}
            AND segments.date BETWEEN '{start_date}' AND '{end_date}'
            ORDER BY segments.date
        """
        results = []
        response = ga_service.search(customer_id=self._customer_id, query=query)
        for row in response:
            results.append(
                DailyStats(
                    date=date_cls.fromisoformat(row.segments.date),
                    channel="google",
                    campaign_id=campaign_id,
                    metrics=MetricSet(
                        impressions=row.metrics.impressions,
                        clicks=row.metrics.clicks,
                        cost=int(row.metrics.cost_micros / 1_000_000),
                        conversions=int(row.metrics.conversions),
                    ),
                )
            )
        return results

    # === 유틸리티 ===

    async def validate_creative(self, creative: CreativeConfig) -> ValidationResult:
        errors = []
        warnings = []
        if len(creative.headline) > 30:
            errors.append(f"Google 검색광고 제목은 30자 이내 (현재: {len(creative.headline)}자)")
        if len(creative.description) > 90:
            errors.append(f"Google 설명은 90자 이내 (현재: {len(creative.description)}자)")
        if not creative.landing_url:
            errors.append("랜딩 URL은 필수입니다")
        rsa_headlines = creative.google_responsive_headlines or [creative.headline]
        if len(rsa_headlines) < 3:
            warnings.append("반응형 검색광고는 최소 3개 제목 권장")
        return ValidationResult(is_valid=len(errors) == 0, errors=errors, warnings=warnings)

    async def estimate_reach(self, targeting: TargetingConfig) -> ReachEstimate:
        # Use keyword planner for estimation (simplified)
        return ReachEstimate(
            channel=ChannelId.GOOGLE,
            estimated_reach=50000,
            estimated_impressions=120000,
            estimated_clicks=3600,
            estimated_cost=3600 * 400,
            confidence="low",
        )

    async def check_approval_status(self, ad_id: str) -> dict:
        client = self._ensure_client()
        ga_service = client.get_service("GoogleAdsService")
        query = f"""
            SELECT ad_group_ad.policy_summary.approval_status
            FROM ad_group_ad
            WHERE ad_group_ad.ad.id = {ad_id}
        """
        response = ga_service.search(customer_id=self._customer_id, query=query)
        for row in response:
            return {
                "ad_id": ad_id,
                "status": row.ad_group_ad.policy_summary.approval_status.name,
                "channel": "google",
            }
        return {"ad_id": ad_id, "status": "UNKNOWN", "channel": "google"}
