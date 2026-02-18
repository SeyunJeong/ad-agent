"""Channel-related models."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ChannelId(str, Enum):
    NAVER = "naver"
    KAKAO = "kakao"
    META = "meta"
    GOOGLE = "google"


class ChannelInfo(BaseModel):
    id: ChannelId
    name: str
    currency: str = "KRW"
    timezone: str = "Asia/Seoul"
    api_version: str
    is_configured: bool = False
    supported_ad_types: list[str] = Field(default_factory=list)
    min_daily_budget: Optional[int] = None
    min_bid: Optional[int] = None


class TargetingConfig(BaseModel):
    """채널 공통 타겟팅 설정."""

    age_range: Optional[str] = None
    gender: str = "all"
    locations: list[str] = Field(default_factory=list)
    interests: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    devices: list[str] = Field(default_factory=lambda: ["mobile", "desktop"])
    schedule: Optional[dict] = None  # {"days": [...], "hours": [...]}
    placements: list[str] = Field(default_factory=list)

    # Naver-specific
    naver_audience_type: Optional[str] = None  # "search" | "display"

    # Meta-specific
    meta_custom_audiences: list[str] = Field(default_factory=list)
    meta_lookalike_source: Optional[str] = None

    # Google-specific
    google_audience_segments: list[str] = Field(default_factory=list)


class Keyword(BaseModel):
    text: str
    match_type: str = "broad"  # "exact" | "phrase" | "broad"
    bid: Optional[int] = None
    channel: Optional[ChannelId] = None
    monthly_searches: Optional[int] = None
    competition: Optional[str] = None  # "low" | "medium" | "high"


class ValidationResult(BaseModel):
    is_valid: bool
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class ReachEstimate(BaseModel):
    channel: ChannelId
    estimated_reach: int
    estimated_impressions: int
    estimated_clicks: int
    estimated_cost: int
    confidence: str = "medium"
