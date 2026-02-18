"""Creative and ad copy models."""

from datetime import datetime
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class CreativeConfig(BaseModel):
    """광고 소재 설정."""

    headline: str = Field(..., max_length=30, description="광고 제목")
    description: str = Field(..., max_length=90, description="광고 설명")
    long_description: Optional[str] = Field(None, max_length=250)
    display_url: Optional[str] = None
    landing_url: str
    call_to_action: Optional[str] = None  # "설치하기", "자세히 보기", etc.
    image_url: Optional[str] = None
    video_url: Optional[str] = None

    # Channel-specific extensions
    naver_extensions: Optional[dict] = None  # phone, location, price, etc.
    meta_format: Optional[str] = None  # "single_image" | "carousel" | "video"
    google_responsive_headlines: list[str] = Field(default_factory=list)
    google_responsive_descriptions: list[str] = Field(default_factory=list)


class CreativeAsset(BaseModel):
    id: str = Field(default_factory=lambda: f"crt_{uuid4().hex[:12]}")
    campaign_id: str
    channel: str
    config: CreativeConfig
    status: str = "draft"  # "draft" | "review" | "approved" | "rejected" | "active"
    review_notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)


class CreativeVariation(BaseModel):
    """A/B 테스트용 변형."""

    id: str = Field(default_factory=lambda: f"var_{uuid4().hex[:12]}")
    parent_creative_id: str
    variation_name: str  # "A", "B", "C"
    config: CreativeConfig
    impressions: int = 0
    clicks: int = 0
    conversions: int = 0
    cost: int = 0

    @property
    def ctr(self) -> float:
        return (self.clicks / self.impressions * 100) if self.impressions > 0 else 0.0

    @property
    def cvr(self) -> float:
        return (self.conversions / self.clicks * 100) if self.clicks > 0 else 0.0


class CreativeGenerationRequest(BaseModel):
    """AI 광고 카피 생성 요청."""

    campaign_id: str
    channels: list[str]
    product_description: str
    target_audience: str
    tone: str = "professional"  # "professional" | "casual" | "urgent" | "witty"
    key_benefits: list[str] = Field(default_factory=list)
    competitors: list[str] = Field(default_factory=list)
    variations_count: int = Field(default=3, ge=1, le=10)


class CreativeReviewResult(BaseModel):
    creative_id: str
    status: str  # "PASS" | "REVISE" | "REJECT"
    legal_issues: list[str] = Field(default_factory=list)
    policy_issues: list[str] = Field(default_factory=list)
    improvement_suggestions: list[str] = Field(default_factory=list)
