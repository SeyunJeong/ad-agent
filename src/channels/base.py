"""Abstract base class for all channel adapters."""

from abc import ABC, abstractmethod
from typing import Any, Optional

from src.models.campaign import Ad, AdGroup, AdGroupConfig, BidStrategy, BudgetConfig, Campaign, CampaignConfig
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


class ChannelAdapter(ABC):
    """IChannelAdapter — 모든 채널 어댑터의 공통 인터페이스.

    plugin/adapters.md에 정의된 32개 메서드를 Python ABC로 구현.
    """

    @abstractmethod
    def channel_id(self) -> ChannelId:
        ...

    @abstractmethod
    async def get_channel_info(self) -> ChannelInfo:
        ...

    @abstractmethod
    async def is_configured(self) -> bool:
        ...

    # === 캠페인 관리 ===

    @abstractmethod
    async def create_campaign(self, config: CampaignConfig) -> dict[str, Any]:
        """채널에 캠페인을 생성하고 채널 고유 ID를 반환."""
        ...

    @abstractmethod
    async def update_campaign(self, channel_campaign_id: str, updates: dict) -> dict:
        ...

    @abstractmethod
    async def pause_campaign(self, channel_campaign_id: str) -> None:
        ...

    @abstractmethod
    async def resume_campaign(self, channel_campaign_id: str) -> None:
        ...

    @abstractmethod
    async def delete_campaign(self, channel_campaign_id: str) -> None:
        ...

    @abstractmethod
    async def get_campaign(self, channel_campaign_id: str) -> dict:
        ...

    @abstractmethod
    async def list_campaigns(self) -> list[dict]:
        ...

    # === 광고 그룹 관리 ===

    @abstractmethod
    async def create_ad_group(self, campaign_id: str, config: AdGroupConfig) -> dict:
        ...

    @abstractmethod
    async def update_ad_group(self, ad_group_id: str, updates: dict) -> dict:
        ...

    @abstractmethod
    async def list_ad_groups(self, campaign_id: str) -> list[dict]:
        ...

    # === 광고/소재 관리 ===

    @abstractmethod
    async def create_ad(self, ad_group_id: str, creative: CreativeConfig) -> dict:
        ...

    @abstractmethod
    async def update_ad(self, ad_id: str, updates: dict) -> dict:
        ...

    @abstractmethod
    async def list_ads(self, ad_group_id: str) -> list[dict]:
        ...

    # === 키워드/타겟팅 ===

    @abstractmethod
    async def add_keywords(self, ad_group_id: str, keywords: list[Keyword]) -> list[dict]:
        ...

    @abstractmethod
    async def remove_keywords(self, ad_group_id: str, keyword_ids: list[str]) -> None:
        ...

    @abstractmethod
    async def set_targeting(self, ad_group_id: str, targeting: TargetingConfig) -> dict:
        ...

    # === 입찰/예산 ===

    @abstractmethod
    async def set_bid_strategy(self, campaign_id: str, strategy: BidStrategy) -> None:
        ...

    @abstractmethod
    async def set_budget(self, campaign_id: str, budget: BudgetConfig) -> None:
        ...

    @abstractmethod
    async def adjust_bid(self, entity_id: str, bid_amount: int) -> None:
        ...

    # === 성과 데이터 ===

    @abstractmethod
    async def get_performance(
        self,
        campaign_id: str,
        start_date: str,
        end_date: str,
    ) -> MetricSet:
        ...

    @abstractmethod
    async def get_daily_stats(
        self,
        campaign_id: str,
        start_date: str,
        end_date: str,
    ) -> list[DailyStats]:
        ...

    # === 유틸리티 ===

    @abstractmethod
    async def validate_creative(self, creative: CreativeConfig) -> ValidationResult:
        ...

    @abstractmethod
    async def estimate_reach(self, targeting: TargetingConfig) -> ReachEstimate:
        ...

    @abstractmethod
    async def check_approval_status(self, ad_id: str) -> dict:
        ...
