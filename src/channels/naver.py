"""Naver Search Ads API adapter.

API: https://api.searchad.naver.com
Auth: HMAC-SHA256 signature
Docs: https://naver.github.io/searchad-apidoc/
"""

import hashlib
import hmac
import time
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

BASE_URL = "https://api.searchad.naver.com"


class NaverSearchAdsAdapter(ChannelAdapter):
    """네이버 검색광고 API 어댑터.

    인증: HMAC-SHA256 (API Key + Secret Key + Customer ID).
    Rate Limit: 1,000 requests / 10초.
    """

    def __init__(
        self,
        api_key: str | None = None,
        secret_key: str | None = None,
        customer_id: str | None = None,
    ) -> None:
        self._api_key = api_key or ""
        self._secret_key = secret_key or ""
        self._customer_id = customer_id or ""
        self._client = httpx.AsyncClient(base_url=BASE_URL, timeout=30.0)

    def channel_id(self) -> ChannelId:
        return ChannelId.NAVER

    async def is_configured(self) -> bool:
        return bool(self._api_key and self._secret_key and self._customer_id)

    async def get_channel_info(self) -> ChannelInfo:
        return ChannelInfo(
            id=ChannelId.NAVER,
            name="네이버 검색광고",
            api_version="2024",
            is_configured=await self.is_configured(),
            supported_ad_types=["파워링크", "쇼핑검색", "브랜드검색", "파워콘텐츠"],
            min_daily_budget=10000,
            min_bid=70,
        )

    def _generate_signature(self, timestamp: str, method: str, path: str) -> str:
        """HMAC-SHA256 서명 생성."""
        message = f"{timestamp}.{method}.{path}"
        signature = hmac.new(
            self._secret_key.encode("utf-8"),
            message.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return signature

    def _headers(self, method: str, path: str) -> dict[str, str]:
        timestamp = str(int(time.time() * 1000))
        signature = self._generate_signature(timestamp, method, path)
        return {
            "X-Timestamp": timestamp,
            "X-API-KEY": self._api_key,
            "X-Customer": self._customer_id,
            "X-Signature": signature,
            "Content-Type": "application/json; charset=UTF-8",
        }

    async def _request(
        self,
        method: str,
        path: str,
        json_data: dict | None = None,
        params: dict | None = None,
    ) -> Any:
        headers = self._headers(method.upper(), path)
        response = await self._client.request(
            method=method,
            url=path,
            headers=headers,
            json=json_data,
            params=params,
        )
        response.raise_for_status()
        return response.json() if response.content else None

    # === 캠페인 관리 ===

    async def create_campaign(self, config: CampaignConfig) -> dict[str, Any]:
        naver_alloc = next(
            (a for a in config.channel_allocations if a.channel == "naver"), None
        )
        payload = {
            "name": config.name,
            "campaignTp": "WEB_SITE",
            "customerId": self._customer_id,
            "dailyBudget": naver_alloc.budget_amount // config.brief.budget.period_days
            if naver_alloc
            else config.brief.budget.daily_budget,
            "deliveryMethod": "STANDARD",
            "userLock": False,
        }
        result = await self._request("POST", "/ncc/campaigns", json_data=payload)
        logger.info("naver_campaign_created", campaign_id=result.get("nccCampaignId"))
        return result

    async def update_campaign(self, channel_campaign_id: str, updates: dict) -> dict:
        payload = {"nccCampaignId": channel_campaign_id, **updates}
        return await self._request("PUT", f"/ncc/campaigns/{channel_campaign_id}", json_data=payload)

    async def pause_campaign(self, channel_campaign_id: str) -> None:
        await self.update_campaign(channel_campaign_id, {"userLock": True})

    async def resume_campaign(self, channel_campaign_id: str) -> None:
        await self.update_campaign(channel_campaign_id, {"userLock": False})

    async def delete_campaign(self, channel_campaign_id: str) -> None:
        await self._request("DELETE", f"/ncc/campaigns/{channel_campaign_id}")

    async def get_campaign(self, channel_campaign_id: str) -> dict:
        return await self._request("GET", f"/ncc/campaigns/{channel_campaign_id}")

    async def list_campaigns(self) -> list[dict]:
        return await self._request("GET", "/ncc/campaigns")

    # === 광고 그룹 ===

    async def create_ad_group(self, campaign_id: str, config: AdGroupConfig) -> dict:
        payload = {
            "nccCampaignId": campaign_id,
            "name": config.name,
            "adGroupType": "KEYWORD",
            "mobileChannelId": "MOBILE",
            "pcChannelId": "PC",
            "dailyBudget": config.daily_budget or 0,
            "bidAmt": 300,  # default starting bid
        }
        return await self._request("POST", "/ncc/adgroups", json_data=payload)

    async def update_ad_group(self, ad_group_id: str, updates: dict) -> dict:
        payload = {"nccAdgroupId": ad_group_id, **updates}
        return await self._request("PUT", f"/ncc/adgroups/{ad_group_id}", json_data=payload)

    async def list_ad_groups(self, campaign_id: str) -> list[dict]:
        return await self._request("GET", "/ncc/adgroups", params={"nccCampaignId": campaign_id})

    # === 광고/소재 ===

    async def create_ad(self, ad_group_id: str, creative: CreativeConfig) -> dict:
        payload = {
            "nccAdgroupId": ad_group_id,
            "type": 1,  # text ad
            "ad": {
                "headline": creative.headline,
                "description": creative.description,
                "pc": {"final": creative.landing_url},
                "mobile": {"final": creative.landing_url},
            },
        }
        return await self._request("POST", "/ncc/ads", json_data=payload)

    async def update_ad(self, ad_id: str, updates: dict) -> dict:
        payload = {"nccAdId": ad_id, **updates}
        return await self._request("PUT", f"/ncc/ads/{ad_id}", json_data=payload)

    async def list_ads(self, ad_group_id: str) -> list[dict]:
        return await self._request("GET", "/ncc/ads", params={"nccAdgroupId": ad_group_id})

    # === 키워드 ===

    async def add_keywords(self, ad_group_id: str, keywords: list[Keyword]) -> list[dict]:
        payload = [
            {
                "nccAdgroupId": ad_group_id,
                "keyword": kw.text,
                "bidAmt": kw.bid or 300,
                "useGroupBidAmt": kw.bid is None,
            }
            for kw in keywords
        ]
        return await self._request("POST", "/ncc/keywords", json_data=payload)

    async def remove_keywords(self, ad_group_id: str, keyword_ids: list[str]) -> None:
        ids = ",".join(keyword_ids)
        await self._request("DELETE", f"/ncc/keywords?ids={ids}")

    async def set_targeting(self, ad_group_id: str, targeting: TargetingConfig) -> dict:
        # Naver targeting is primarily keyword-based + schedule
        updates: dict[str, Any] = {}
        if targeting.schedule:
            updates["schedules"] = targeting.schedule
        if targeting.devices:
            device_map = {"mobile": "MOBILE", "desktop": "PC"}
            updates["targets"] = {
                "pc": "PC" in [device_map.get(d, d) for d in targeting.devices],
                "mobile": "MOBILE" in [device_map.get(d, d) for d in targeting.devices],
            }
        return await self.update_ad_group(ad_group_id, updates)

    # === 입찰/예산 ===

    async def set_bid_strategy(self, campaign_id: str, strategy: BidStrategy) -> None:
        # Naver uses manual CPC primarily
        updates = {}
        if strategy.strategy_type == "manual_cpc" and strategy.max_bid:
            updates["bidAmt"] = strategy.max_bid
        await self.update_campaign(campaign_id, updates)

    async def set_budget(self, campaign_id: str, budget: BudgetConfig) -> None:
        await self.update_campaign(campaign_id, {"dailyBudget": budget.daily_budget})

    async def adjust_bid(self, entity_id: str, bid_amount: int) -> None:
        await self._request(
            "PUT",
            f"/ncc/keywords/{entity_id}",
            json_data={"nccKeywordId": entity_id, "bidAmt": bid_amount},
        )

    # === 성과 데이터 ===

    async def get_performance(
        self,
        campaign_id: str,
        start_date: str,
        end_date: str,
    ) -> MetricSet:
        params = {
            "id": campaign_id,
            "fields": '["impCnt","clkCnt","salesAmt","ccnt"]',
            "timeRange": f'{{"since":"{start_date}","until":"{end_date}"}}',
        }
        data = await self._request("GET", "/stat-reports", params=params)
        if not data:
            return MetricSet()
        row = data[0] if isinstance(data, list) else data
        return MetricSet(
            impressions=row.get("impCnt", 0),
            clicks=row.get("clkCnt", 0),
            cost=row.get("salesAmt", 0),
            conversions=row.get("ccnt", 0),
        )

    async def get_daily_stats(
        self,
        campaign_id: str,
        start_date: str,
        end_date: str,
    ) -> list[DailyStats]:
        params = {
            "id": campaign_id,
            "fields": '["impCnt","clkCnt","salesAmt","ccnt"]',
            "timeRange": f'{{"since":"{start_date}","until":"{end_date}"}}',
            "datePreset": "allDays",
        }
        data = await self._request("GET", "/stat-reports", params=params)
        if not data:
            return []
        from datetime import date as date_cls

        return [
            DailyStats(
                date=date_cls.fromisoformat(row.get("statDt", start_date)),
                channel="naver",
                campaign_id=campaign_id,
                metrics=MetricSet(
                    impressions=row.get("impCnt", 0),
                    clicks=row.get("clkCnt", 0),
                    cost=row.get("salesAmt", 0),
                    conversions=row.get("ccnt", 0),
                ),
            )
            for row in (data if isinstance(data, list) else [data])
        ]

    # === 키워드 도구 ===

    async def get_keyword_suggestions(self, keyword: str) -> list[dict]:
        """네이버 키워드 도구 — 검색량, 경쟁도 조회."""
        payload = {
            "siteId": "",
            "biztpId": 0,
            "hintKeywords": [keyword],
            "event": 0,
            "month": 0,
            "showDetail": 1,
        }
        return await self._request("POST", "/keywordstool", json_data=payload)

    # === 유틸리티 ===

    async def validate_creative(self, creative: CreativeConfig) -> ValidationResult:
        errors = []
        warnings = []
        if len(creative.headline) > 15:
            errors.append(f"네이버 파워링크 제목은 15자 이내 (현재: {len(creative.headline)}자)")
        if len(creative.description) > 45:
            errors.append(f"네이버 파워링크 설명은 45자 이내 (현재: {len(creative.description)}자)")
        if not creative.landing_url:
            errors.append("랜딩 URL은 필수입니다")
        return ValidationResult(is_valid=len(errors) == 0, errors=errors, warnings=warnings)

    async def estimate_reach(self, targeting: TargetingConfig) -> ReachEstimate:
        # Use keyword tool for estimation
        total_searches = 0
        for kw in targeting.keywords[:10]:
            suggestions = await self.get_keyword_suggestions(kw)
            if suggestions:
                total_searches += suggestions[0].get("monthlyPcQcCnt", 0)
                total_searches += suggestions[0].get("monthlyMobileQcCnt", 0)
        estimated_clicks = int(total_searches * 0.03)  # ~3% CTR assumption
        return ReachEstimate(
            channel=ChannelId.NAVER,
            estimated_reach=total_searches,
            estimated_impressions=total_searches,
            estimated_clicks=estimated_clicks,
            estimated_cost=estimated_clicks * 300,  # avg CPC 300원
        )

    async def check_approval_status(self, ad_id: str) -> dict:
        ad_data = await self._request("GET", f"/ncc/ads/{ad_id}")
        return {
            "ad_id": ad_id,
            "status": ad_data.get("inspectStatus", "UNKNOWN"),
            "channel": "naver",
        }

    async def close(self) -> None:
        await self._client.aclose()
