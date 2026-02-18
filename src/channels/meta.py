"""Meta (Facebook/Instagram) Ads API adapter.

Uses the official facebook-business Python SDK.
API: https://developers.facebook.com/docs/marketing-apis
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


class MetaAdsAdapter(ChannelAdapter):
    """Meta Ads (Facebook/Instagram) 어댑터.

    facebook-business SDK를 사용한 실제 API 통신.
    """

    def __init__(
        self,
        app_id: str | None = None,
        app_secret: str | None = None,
        access_token: str | None = None,
        ad_account_id: str | None = None,
    ) -> None:
        self._app_id = app_id or ""
        self._app_secret = app_secret or ""
        self._access_token = access_token or ""
        self._ad_account_id = ad_account_id or ""
        self._api = None
        self._ad_account = None

    def _ensure_sdk(self) -> None:
        """Lazy-init Facebook SDK."""
        if self._api is not None:
            return
        from facebook_business.api import FacebookAdsApi
        from facebook_business.adobjects.adaccount import AdAccount

        self._api = FacebookAdsApi.init(
            self._app_id,
            self._app_secret,
            self._access_token,
        )
        self._ad_account = AdAccount(self._ad_account_id)

    def channel_id(self) -> ChannelId:
        return ChannelId.META

    async def is_configured(self) -> bool:
        return bool(self._access_token and self._ad_account_id)

    async def get_channel_info(self) -> ChannelInfo:
        return ChannelInfo(
            id=ChannelId.META,
            name="Meta (Facebook/Instagram)",
            api_version="v21.0",
            is_configured=await self.is_configured(),
            supported_ad_types=[
                "single_image",
                "carousel",
                "video",
                "stories",
                "reels",
            ],
            min_daily_budget=1000,
            min_bid=100,
        )

    # === 캠페인 관리 ===

    async def create_campaign(self, config: CampaignConfig) -> dict[str, Any]:
        self._ensure_sdk()
        from facebook_business.adobjects.campaign import Campaign as FbCampaign

        objective_map = {
            "awareness": "OUTCOME_AWARENESS",
            "consideration": "OUTCOME_ENGAGEMENT",
            "conversion": "OUTCOME_SALES",
            "app_install": "OUTCOME_APP_PROMOTION",
            "lead_generation": "OUTCOME_LEADS",
        }
        meta_alloc = next(
            (a for a in config.channel_allocations if a.channel == "meta"), None
        )
        params = {
            "name": config.name,
            "objective": objective_map.get(
                config.brief.objective.value, "OUTCOME_AWARENESS"
            ),
            "status": "PAUSED",
            "special_ad_categories": [],
        }
        if meta_alloc:
            params["daily_budget"] = str(
                meta_alloc.budget_amount // config.brief.budget.period_days
            )

        result = self._ad_account.create_campaign(params=params)
        logger.info("meta_campaign_created", campaign_id=result["id"])
        return {"id": result["id"], "status": "PAUSED"}

    async def update_campaign(self, channel_campaign_id: str, updates: dict) -> dict:
        self._ensure_sdk()
        from facebook_business.adobjects.campaign import Campaign as FbCampaign

        campaign = FbCampaign(channel_campaign_id)
        campaign.api_update(params=updates)
        return {"id": channel_campaign_id, "updated": True}

    async def pause_campaign(self, channel_campaign_id: str) -> None:
        await self.update_campaign(channel_campaign_id, {"status": "PAUSED"})

    async def resume_campaign(self, channel_campaign_id: str) -> None:
        await self.update_campaign(channel_campaign_id, {"status": "ACTIVE"})

    async def delete_campaign(self, channel_campaign_id: str) -> None:
        await self.update_campaign(channel_campaign_id, {"status": "DELETED"})

    async def get_campaign(self, channel_campaign_id: str) -> dict:
        self._ensure_sdk()
        from facebook_business.adobjects.campaign import Campaign as FbCampaign

        campaign = FbCampaign(channel_campaign_id)
        data = campaign.api_get(
            fields=["name", "status", "objective", "daily_budget", "lifetime_budget"]
        )
        return dict(data)

    async def list_campaigns(self) -> list[dict]:
        self._ensure_sdk()
        campaigns = self._ad_account.get_campaigns(
            fields=["name", "status", "objective", "daily_budget"]
        )
        return [dict(c) for c in campaigns]

    # === 광고 세트 (Ad Set = Ad Group) ===

    async def create_ad_group(self, campaign_id: str, config: AdGroupConfig) -> dict:
        self._ensure_sdk()
        params = {
            "name": config.name,
            "campaign_id": campaign_id,
            "billing_event": "IMPRESSIONS",
            "optimization_goal": "LINK_CLICKS",
            "daily_budget": str(config.daily_budget or 10000),
            "status": "PAUSED",
            "targeting": self._build_targeting(config.targeting),
        }
        result = self._ad_account.create_ad_set(params=params)
        return {"id": result["id"]}

    async def update_ad_group(self, ad_group_id: str, updates: dict) -> dict:
        self._ensure_sdk()
        from facebook_business.adobjects.adset import AdSet

        ad_set = AdSet(ad_group_id)
        ad_set.api_update(params=updates)
        return {"id": ad_group_id, "updated": True}

    async def list_ad_groups(self, campaign_id: str) -> list[dict]:
        self._ensure_sdk()
        from facebook_business.adobjects.campaign import Campaign as FbCampaign

        campaign = FbCampaign(campaign_id)
        ad_sets = campaign.get_ad_sets(fields=["name", "status", "daily_budget"])
        return [dict(a) for a in ad_sets]

    # === 광고 소재 ===

    async def create_ad(self, ad_group_id: str, creative: CreativeConfig) -> dict:
        self._ensure_sdk()
        # First create AdCreative
        creative_params = {
            "name": creative.headline,
            "object_story_spec": {
                "page_id": "",  # needs page ID
                "link_data": {
                    "message": creative.description,
                    "link": creative.landing_url,
                    "name": creative.headline,
                    "call_to_action": {
                        "type": self._map_cta(creative.call_to_action),
                        "value": {"link": creative.landing_url},
                    },
                },
            },
        }
        if creative.image_url:
            creative_params["object_story_spec"]["link_data"][
                "picture"
            ] = creative.image_url

        ad_creative = self._ad_account.create_ad_creative(params=creative_params)

        # Then create Ad
        ad_params = {
            "name": creative.headline,
            "adset_id": ad_group_id,
            "creative": {"creative_id": ad_creative["id"]},
            "status": "PAUSED",
        }
        result = self._ad_account.create_ad(params=ad_params)
        return {"id": result["id"], "creative_id": ad_creative["id"]}

    async def update_ad(self, ad_id: str, updates: dict) -> dict:
        self._ensure_sdk()
        from facebook_business.adobjects.ad import Ad

        ad = Ad(ad_id)
        ad.api_update(params=updates)
        return {"id": ad_id, "updated": True}

    async def list_ads(self, ad_group_id: str) -> list[dict]:
        self._ensure_sdk()
        from facebook_business.adobjects.adset import AdSet

        ad_set = AdSet(ad_group_id)
        ads = ad_set.get_ads(fields=["name", "status", "creative"])
        return [dict(a) for a in ads]

    # === 키워드/타겟팅 ===

    async def add_keywords(
        self, ad_group_id: str, keywords: list[Keyword]
    ) -> list[dict]:
        # Meta doesn't use keywords — targeting is interest-based
        logger.warning("meta_no_keyword_support", msg="Meta uses interest targeting, not keywords")
        return []

    async def remove_keywords(
        self, ad_group_id: str, keyword_ids: list[str]
    ) -> None:
        pass  # Not applicable for Meta

    async def set_targeting(
        self, ad_group_id: str, targeting: TargetingConfig
    ) -> dict:
        meta_targeting = self._build_targeting(targeting)
        return await self.update_ad_group(
            ad_group_id, {"targeting": meta_targeting}
        )

    def _build_targeting(self, targeting: Any) -> dict:
        """TargetingConfig → Meta targeting spec."""
        if targeting is None:
            return {"geo_locations": {"countries": ["KR"]}}

        spec: dict[str, Any] = {"geo_locations": {"countries": ["KR"]}}

        if targeting.age_range:
            parts = targeting.age_range.split("-")
            if len(parts) == 2:
                spec["age_min"] = int(parts[0])
                spec["age_max"] = int(parts[1])

        if targeting.gender != "all":
            spec["genders"] = [1] if targeting.gender == "male" else [2]

        if targeting.interests:
            spec["flexible_spec"] = [
                {"interests": [{"name": i} for i in targeting.interests]}
            ]

        if targeting.devices:
            device_map = {"mobile": ["Android", "iOS"], "desktop": []}
            user_os = []
            for d in targeting.devices:
                user_os.extend(device_map.get(d, []))
            if user_os:
                spec["user_os"] = user_os

        if targeting.meta_custom_audiences:
            spec["custom_audiences"] = [
                {"id": a} for a in targeting.meta_custom_audiences
            ]

        return spec

    def _map_cta(self, cta: str | None) -> str:
        cta_map = {
            "설치하기": "INSTALL_MOBILE_APP",
            "자세히 보기": "LEARN_MORE",
            "지금 구매": "SHOP_NOW",
            "가입하기": "SIGN_UP",
        }
        return cta_map.get(cta or "", "LEARN_MORE")

    # === 입찰/예산 ===

    async def set_bid_strategy(
        self, campaign_id: str, strategy: BidStrategy
    ) -> None:
        strategy_map = {
            "manual_cpc": "LOWEST_COST_WITHOUT_CAP",
            "target_cpa": "COST_CAP",
            "maximize_conversions": "LOWEST_COST_WITHOUT_CAP",
            "target_roas": "MINIMUM_ROAS",
        }
        updates = {
            "bid_strategy": strategy_map.get(
                strategy.strategy_type, "LOWEST_COST_WITHOUT_CAP"
            )
        }
        if strategy.target_value and strategy.strategy_type == "target_cpa":
            updates["bid_amount"] = str(int(strategy.target_value))
        await self.update_campaign(campaign_id, updates)

    async def set_budget(self, campaign_id: str, budget: BudgetConfig) -> None:
        await self.update_campaign(
            campaign_id, {"daily_budget": str(budget.daily_budget)}
        )

    async def adjust_bid(self, entity_id: str, bid_amount: int) -> None:
        await self.update_ad_group(entity_id, {"bid_amount": str(bid_amount)})

    # === 성과 데이터 ===

    async def get_performance(
        self,
        campaign_id: str,
        start_date: str,
        end_date: str,
    ) -> MetricSet:
        self._ensure_sdk()
        from facebook_business.adobjects.campaign import Campaign as FbCampaign

        campaign = FbCampaign(campaign_id)
        insights = campaign.get_insights(
            params={
                "time_range": {"since": start_date, "until": end_date},
                "fields": [
                    "impressions",
                    "clicks",
                    "spend",
                    "actions",
                ],
            }
        )
        if not insights:
            return MetricSet()

        row = dict(insights[0])
        conversions = 0
        for action in row.get("actions", []):
            if action.get("action_type") in (
                "app_install",
                "purchase",
                "lead",
                "complete_registration",
            ):
                conversions += int(action.get("value", 0))

        return MetricSet(
            impressions=int(row.get("impressions", 0)),
            clicks=int(row.get("clicks", 0)),
            cost=int(float(row.get("spend", 0))),
            conversions=conversions,
        )

    async def get_daily_stats(
        self,
        campaign_id: str,
        start_date: str,
        end_date: str,
    ) -> list[DailyStats]:
        self._ensure_sdk()
        from datetime import date as date_cls

        from facebook_business.adobjects.campaign import Campaign as FbCampaign

        campaign = FbCampaign(campaign_id)
        insights = campaign.get_insights(
            params={
                "time_range": {"since": start_date, "until": end_date},
                "time_increment": 1,
                "fields": ["impressions", "clicks", "spend", "actions"],
            }
        )
        results = []
        for row_data in insights:
            row = dict(row_data)
            conversions = 0
            for action in row.get("actions", []):
                if action.get("action_type") in (
                    "app_install",
                    "purchase",
                    "lead",
                ):
                    conversions += int(action.get("value", 0))

            results.append(
                DailyStats(
                    date=date_cls.fromisoformat(row.get("date_start", start_date)),
                    channel="meta",
                    campaign_id=campaign_id,
                    metrics=MetricSet(
                        impressions=int(row.get("impressions", 0)),
                        clicks=int(row.get("clicks", 0)),
                        cost=int(float(row.get("spend", 0))),
                        conversions=conversions,
                    ),
                )
            )
        return results

    # === 유틸리티 ===

    async def validate_creative(self, creative: CreativeConfig) -> ValidationResult:
        errors = []
        warnings = []
        if len(creative.headline) > 25:
            errors.append(f"Meta 광고 제목은 25자 이내 권장 (현재: {len(creative.headline)}자)")
        if len(creative.description) > 125:
            warnings.append(f"Meta 설명은 125자 이내 권장 (현재: {len(creative.description)}자)")
        if not creative.landing_url:
            errors.append("랜딩 URL은 필수입니다")
        # 20% text rule warning for images
        if creative.image_url:
            warnings.append("이미지 내 텍스트 비율 20% 초과 시 노출 제한될 수 있습니다")
        return ValidationResult(is_valid=len(errors) == 0, errors=errors, warnings=warnings)

    async def estimate_reach(self, targeting: TargetingConfig) -> ReachEstimate:
        self._ensure_sdk()
        spec = self._build_targeting(targeting)
        try:
            result = self._ad_account.get_reach_estimate(
                params={"targeting_spec": spec}
            )
            data = dict(result[0]) if result else {}
            users = data.get("users", 100000)
        except Exception:
            users = 100000  # fallback estimate

        return ReachEstimate(
            channel=ChannelId.META,
            estimated_reach=users,
            estimated_impressions=int(users * 2.5),
            estimated_clicks=int(users * 2.5 * 0.01),
            estimated_cost=int(users * 2.5 * 0.01 * 200),
        )

    async def check_approval_status(self, ad_id: str) -> dict:
        self._ensure_sdk()
        from facebook_business.adobjects.ad import Ad

        ad = Ad(ad_id)
        data = ad.api_get(fields=["effective_status", "review_feedback"])
        return {
            "ad_id": ad_id,
            "status": data.get("effective_status", "UNKNOWN"),
            "feedback": data.get("review_feedback", {}),
            "channel": "meta",
        }
