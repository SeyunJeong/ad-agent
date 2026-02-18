"""Campaign domain models."""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class CampaignStatus(str, Enum):
    DRAFT = "draft"
    PLANNING = "planning"
    READY = "ready"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class CampaignObjective(str, Enum):
    AWARENESS = "awareness"
    CONSIDERATION = "consideration"
    CONVERSION = "conversion"
    APP_INSTALL = "app_install"
    LEAD_GENERATION = "lead_generation"


class Industry(str, Enum):
    ECOMMERCE = "ecommerce"
    ECOMMERCE_FASHION = "ecommerce_fashion"
    SAAS = "saas"
    LOCAL_BUSINESS = "local_business"
    APP = "app"
    EDUCATION = "education"
    FINANCE = "finance"
    HEALTHCARE = "healthcare"
    TRAVEL = "travel"
    GAME = "game"
    OTHER = "other"


class TargetAudience(BaseModel):
    age_range: Optional[str] = Field(None, description="예: 25-44")
    gender: str = "all"
    location: str = "전국"
    interests: list[str] = Field(default_factory=list)
    custom_description: Optional[str] = None


class BudgetConfig(BaseModel):
    total_amount: int = Field(..., ge=100000, description="총 예산 (원)")
    period_days: int = Field(..., ge=1, description="캠페인 기간 (일)")
    daily_cap: Optional[int] = Field(None, description="일예산 상한 (원)")
    currency: str = "KRW"

    @property
    def daily_budget(self) -> int:
        if self.daily_cap:
            return self.daily_cap
        return self.total_amount // self.period_days


class KpiTarget(BaseModel):
    primary_kpi: str = Field(..., description="주요 KPI (예: CPA, ROAS, CPI)")
    primary_target: float = Field(..., description="주요 KPI 목표치")
    secondary_kpi: Optional[str] = None
    secondary_target: Optional[float] = None


class CampaignBrief(BaseModel):
    """캠페인 생성 요청 — plugin/interface.md의 Input Schema 구현."""

    business_name: str
    product_service: str
    industry: Industry
    objective: CampaignObjective
    target_audience: TargetAudience
    budget: BudgetConfig
    kpi: KpiTarget
    channels: list[str] = Field(
        default_factory=list,
        description="사용 채널 (비워두면 자동 추천)",
    )
    landing_page: Optional[str] = None
    competitors: list[str] = Field(default_factory=list)
    existing_assets: bool = False
    notes: Optional[str] = None


class BidStrategy(BaseModel):
    strategy_type: str = Field(
        ..., description="manual_cpc | target_cpa | maximize_conversions | target_roas"
    )
    target_value: Optional[float] = None
    max_bid: Optional[int] = None
    min_bid: Optional[int] = None


class ChannelAllocation(BaseModel):
    channel: str
    budget_ratio: float = Field(..., ge=0, le=100)
    budget_amount: int
    objective: str
    ad_types: list[str] = Field(default_factory=list)
    bid_strategy: Optional[BidStrategy] = None
    expected_cpi: Optional[float] = None
    expected_cpa: Optional[float] = None


class CampaignConfig(BaseModel):
    name: str
    brief: CampaignBrief
    channel_allocations: list[ChannelAllocation] = Field(default_factory=list)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class Campaign(BaseModel):
    id: str = Field(default_factory=lambda: f"camp_{uuid4().hex[:12]}")
    config: CampaignConfig
    status: CampaignStatus = CampaignStatus.DRAFT
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    strategy_summary: Optional[str] = None
    risk_assessment: list[dict] = Field(default_factory=list)

    # Channel-specific IDs after launch
    channel_campaign_ids: dict[str, str] = Field(default_factory=dict)


class CampaignFilters(BaseModel):
    status: Optional[CampaignStatus] = None
    channel: Optional[str] = None
    industry: Optional[Industry] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None


class AdGroupConfig(BaseModel):
    name: str
    campaign_id: str
    channel: str
    targeting: Optional[TargetAudience] = None
    bid_strategy: Optional[BidStrategy] = None
    daily_budget: Optional[int] = None


class AdGroup(BaseModel):
    id: str = Field(default_factory=lambda: f"adg_{uuid4().hex[:12]}")
    config: AdGroupConfig
    channel_adgroup_id: Optional[str] = None
    status: str = "active"
    created_at: datetime = Field(default_factory=datetime.now)


class Ad(BaseModel):
    id: str = Field(default_factory=lambda: f"ad_{uuid4().hex[:12]}")
    ad_group_id: str
    channel: str
    headline: str
    description: str
    display_url: Optional[str] = None
    landing_url: Optional[str] = None
    channel_ad_id: Optional[str] = None
    status: str = "active"
    created_at: datetime = Field(default_factory=datetime.now)
