"""Kakao Moment Ads API adapter.

API: https://moment.kakao.com
Auth: OAuth 2.0 Bearer Token
NOTE: Kakao Moment API requires AGENCY registration.
      Individual developer access is NOT available.
      This adapter is implemented and ready for when agency access is obtained.
"""

from typing import Any

import httpx
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

BASE_URL = "https://api.moment.kakao.com"


class KakaoMomentAdapter(ChannelAdapter):
    """카카오 모먼트 광고 어댑터.

    ⚠️ 카카오 모먼트 API는 대행사 등록이 필요합니다.
    개인 개발자 접근 불가 — 대행사 등록 후 사용 가능.
    """

    def __init__(
        self,
        app_key: str | None = None,
        access_token: str | None = None,
        ad_account_id: str | None = None,
    ) -> None:
        self._app_key = app_key or ""
        self._access_token = access_token or ""
        self._ad_account_id = ad_account_id or ""
        self._client = httpx.AsyncClient(base_url=BASE_URL, timeout=30.0)

    def channel_id(self) -> ChannelId:
        return ChannelId.KAKAO

    async def is_configured(self) -> bool:
        return bool(self._app_key and self._access_token and self._ad_account_id)

    async def get_channel_info(self) -> ChannelInfo:
        return ChannelInfo(
            id=ChannelId.KAKAO,
            name="카카오 모먼트",
            api_version="v4",
            is_configured=await self.is_configured(),
            supported_ad_types=[
                "디스플레이",
                "메시지",
                "동영상",
                "카카오비즈보드",
                "쇼핑",
            ],
            min_daily_budget=10000,
            min_bid=50,
        )

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._access_token}",
            "adAccountId": self._ad_account_id,
            "Content-Type": "application/json",
        }

    async def _request(
        self,
        method: str,
        path: str,
        json_data: dict | None = None,
        params: dict | None = None,
    ) -> Any:
        if not await self.is_configured():
            logger.warning("kakao_not_configured", msg="카카오 모먼트 API 미설정 (대행사 등록 필요)")
            return {"error": "not_configured", "message": "카카오 모먼트는 대행사 등록이 필요합니다"}

        response = await self._client.request(
            method=method,
            url=path,
            headers=self._headers(),
            json=json_data,
            params=params,
        )
        response.raise_for_status()
        return response.json() if response.content else None

    # === 캠페인 관리 ===

    async def create_campaign(self, config: CampaignConfig) -> dict[str, Any]:
        objective_map = {
            "awareness": "REACH",
            "consideration": "VISITING",
            "conversion": "CONVERSION",
            "app_install": "APP_INSTALL",
            "lead_generation": "CONVERSION",
        }
        kakao_alloc = next(
            (a for a in config.channel_allocations if a.channel == "kakao"), None
        )
        payload = {
            "name": config.name,
            "campaignTypeGoal": {
                "campaignType": "DISPLAY",
                "goal": objective_map.get(config.brief.objective.value, "VISITING"),
            },
            "dailyBudgetAmount": kakao_alloc.budget_amount // config.brief.budget.period_days
            if kakao_alloc
            else config.brief.budget.daily_budget,
            "config": "ON",
        }
        result = await self._request("POST", "/openapi/v4/campaigns", json_data=payload)
        if result and "id" in result:
            logger.info("kakao_campaign_created", campaign_id=result["id"])
        return result or {}

    async def update_campaign(self, channel_campaign_id: str, updates: dict) -> dict:
        return await self._request(
            "PUT", f"/openapi/v4/campaigns/{channel_campaign_id}", json_data=updates
        ) or {}

    async def pause_campaign(self, channel_campaign_id: str) -> None:
        await self.update_campaign(channel_campaign_id, {"config": "OFF"})

    async def resume_campaign(self, channel_campaign_id: str) -> None:
        await self.update_campaign(channel_campaign_id, {"config": "ON"})

    async def delete_campaign(self, channel_campaign_id: str) -> None:
        await self._request("DELETE", f"/openapi/v4/campaigns/{channel_campaign_id}")

    async def get_campaign(self, channel_campaign_id: str) -> dict:
        return await self._request("GET", f"/openapi/v4/campaigns/{channel_campaign_id}") or {}

    async def list_campaigns(self) -> list[dict]:
        result = await self._request("GET", "/openapi/v4/campaigns")
        return result.get("content", []) if result else []

    # === 광고 그룹 ===

    async def create_ad_group(self, campaign_id: str, config: AdGroupConfig) -> dict:
        payload = {
            "campaignId": campaign_id,
            "name": config.name,
            "dailyBudgetAmount": config.daily_budget or 10000,
            "bidStrategy": {"strategy": "MANUAL_CPC", "bidAmount": 300},
            "config": "ON",
        }
        return await self._request("POST", "/openapi/v4/adGroups", json_data=payload) or {}

    async def update_ad_group(self, ad_group_id: str, updates: dict) -> dict:
        return await self._request(
            "PUT", f"/openapi/v4/adGroups/{ad_group_id}", json_data=updates
        ) or {}

    async def list_ad_groups(self, campaign_id: str) -> list[dict]:
        result = await self._request(
            "GET", "/openapi/v4/adGroups", params={"campaignId": campaign_id}
        )
        return result.get("content", []) if result else []

    # === 광고 소재 ===

    async def create_ad(self, ad_group_id: str, creative: CreativeConfig) -> dict:
        payload = {
            "adGroupId": ad_group_id,
            "name": creative.headline,
            "creative": {
                "title": creative.headline,
                "description": creative.description,
                "landingUrl": creative.landing_url,
                "callToAction": creative.call_to_action or "자세히보기",
            },
            "config": "ON",
        }
        if creative.image_url:
            payload["creative"]["imageUrl"] = creative.image_url
        return await self._request("POST", "/openapi/v4/creatives", json_data=payload) or {}

    async def update_ad(self, ad_id: str, updates: dict) -> dict:
        return await self._request(
            "PUT", f"/openapi/v4/creatives/{ad_id}", json_data=updates
        ) or {}

    async def list_ads(self, ad_group_id: str) -> list[dict]:
        result = await self._request(
            "GET", "/openapi/v4/creatives", params={"adGroupId": ad_group_id}
        )
        return result.get("content", []) if result else []

    # === 키워드/타겟팅 ===

    async def add_keywords(self, ad_group_id: str, keywords: list[Keyword]) -> list[dict]:
        logger.warning("kakao_keyword_limited", msg="카카오 모먼트는 키워드 타겟팅 제한적")
        return []

    async def remove_keywords(self, ad_group_id: str, keyword_ids: list[str]) -> None:
        pass

    async def set_targeting(self, ad_group_id: str, targeting: TargetingConfig) -> dict:
        payload: dict[str, Any] = {}
        if targeting.age_range:
            parts = targeting.age_range.split("-")
            if len(parts) == 2:
                payload["targeting"] = {
                    "age": [{"from": int(parts[0]), "to": int(parts[1])}]
                }
        if targeting.gender != "all":
            gender_map = {"male": "M", "female": "F"}
            if "targeting" not in payload:
                payload["targeting"] = {}
            payload["targeting"]["gender"] = [gender_map.get(targeting.gender, "A")]

        if targeting.locations:
            if "targeting" not in payload:
                payload["targeting"] = {}
            payload["targeting"]["location"] = targeting.locations

        return await self.update_ad_group(ad_group_id, payload)

    # === 입찰/예산 ===

    async def set_bid_strategy(self, campaign_id: str, strategy: BidStrategy) -> None:
        strategy_map = {
            "manual_cpc": "MANUAL_CPC",
            "target_cpa": "AUTO_BID",
            "maximize_conversions": "AUTO_BID",
        }
        await self.update_campaign(
            campaign_id,
            {
                "bidStrategy": {
                    "strategy": strategy_map.get(strategy.strategy_type, "MANUAL_CPC"),
                    "bidAmount": strategy.max_bid or 300,
                }
            },
        )

    async def set_budget(self, campaign_id: str, budget: BudgetConfig) -> None:
        await self.update_campaign(
            campaign_id, {"dailyBudgetAmount": budget.daily_budget}
        )

    async def adjust_bid(self, entity_id: str, bid_amount: int) -> None:
        await self.update_ad_group(
            entity_id, {"bidStrategy": {"bidAmount": bid_amount}}
        )

    # === 성과 데이터 ===

    async def get_performance(
        self,
        campaign_id: str,
        start_date: str,
        end_date: str,
    ) -> MetricSet:
        params = {
            "campaignId": campaign_id,
            "dateStart": start_date,
            "dateEnd": end_date,
            "metricsGroup": "BASIC",
        }
        data = await self._request("GET", "/openapi/v4/report/campaign", params=params)
        if not data or "data" not in data:
            return MetricSet()
        row = data["data"]
        return MetricSet(
            impressions=row.get("imp", 0),
            clicks=row.get("click", 0),
            cost=row.get("spending", 0),
            conversions=row.get("conversion", 0),
        )

    async def get_daily_stats(
        self,
        campaign_id: str,
        start_date: str,
        end_date: str,
    ) -> list[DailyStats]:
        params = {
            "campaignId": campaign_id,
            "dateStart": start_date,
            "dateEnd": end_date,
            "metricsGroup": "BASIC",
            "dimension": "DAY",
        }
        data = await self._request("GET", "/openapi/v4/report/campaign", params=params)
        if not data or "data" not in data:
            return []
        from datetime import date as date_cls

        return [
            DailyStats(
                date=date_cls.fromisoformat(row.get("start", start_date)),
                channel="kakao",
                campaign_id=campaign_id,
                metrics=MetricSet(
                    impressions=row.get("imp", 0),
                    clicks=row.get("click", 0),
                    cost=row.get("spending", 0),
                    conversions=row.get("conversion", 0),
                ),
            )
            for row in (data["data"] if isinstance(data["data"], list) else [data["data"]])
        ]

    # === 유틸리티 ===

    async def validate_creative(self, creative: CreativeConfig) -> ValidationResult:
        errors = []
        warnings = []
        if len(creative.headline) > 25:
            errors.append(f"카카오 광고 제목은 25자 이내 (현재: {len(creative.headline)}자)")
        if len(creative.description) > 45:
            errors.append(f"카카오 설명은 45자 이내 (현재: {len(creative.description)}자)")
        if not creative.landing_url:
            errors.append("랜딩 URL은 필수입니다")
        if not await self.is_configured():
            warnings.append("카카오 모먼트 API가 미설정 상태입니다 (대행사 등록 필요)")
        return ValidationResult(is_valid=len(errors) == 0, errors=errors, warnings=warnings)

    async def estimate_reach(self, targeting: TargetingConfig) -> ReachEstimate:
        return ReachEstimate(
            channel=ChannelId.KAKAO,
            estimated_reach=80000,
            estimated_impressions=200000,
            estimated_clicks=4000,
            estimated_cost=4000 * 250,
            confidence="low",
        )

    async def check_approval_status(self, ad_id: str) -> dict:
        data = await self._request("GET", f"/openapi/v4/creatives/{ad_id}")
        return {
            "ad_id": ad_id,
            "status": data.get("reviewStatus", "UNKNOWN") if data else "UNKNOWN",
            "channel": "kakao",
        }

    async def close(self) -> None:
        await self._client.aclose()
