"""Visual asset models for the visual content generation pipeline."""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class VisualStatus(str, Enum):
    PENDING = "pending"
    GENERATING = "generating"
    COMPOSITING = "compositing"
    DRAFT = "draft"
    APPROVED = "approved"
    REJECTED = "rejected"
    EDITING = "editing"  # Canva editing in progress
    FAILED = "failed"


class AssetType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"
    AVATAR_VIDEO = "avatar_video"
    COMPOSITE = "composite"  # AI image + Korean text overlay


class ChannelFormat(str, Enum):
    """22 channel-specific ad formats."""

    # Naver (5)
    NAVER_SHOPPING_SQUARE = "naver_shopping_1000x1000"
    NAVER_BRAND_BANNER_PC = "naver_brand_750x200"
    NAVER_BRAND_BANNER_MOBILE = "naver_brand_640x300"
    NAVER_DISPLAY = "naver_display_1200x628"
    NAVER_NATIVE = "naver_native_500x500"
    # Kakao (7)
    KAKAO_DISPLAY = "kakao_display_1200x628"
    KAKAO_NATIVE = "kakao_native_500x500"
    KAKAO_BIZBOARD = "kakao_bizboard_1029x258"
    KAKAO_MESSAGE = "kakao_message_800x400"
    KAKAO_VIDEO_LANDSCAPE = "kakao_video_1920x1080"
    KAKAO_VIDEO_SQUARE = "kakao_video_1080x1080"
    KAKAO_VIDEO_VERTICAL = "kakao_video_1080x1920"
    # Meta (5)
    META_FEED_SQUARE = "meta_feed_1080x1080"
    META_FEED_PORTRAIT = "meta_feed_1080x1350"
    META_LINK = "meta_link_1200x628"
    META_REELS = "meta_reels_1080x1920"
    META_CAROUSEL = "meta_carousel_1080x1080"
    # Google (5, reusing some)
    GOOGLE_DISPLAY = "google_display_1200x628"
    GOOGLE_SQUARE = "google_square_1200x1200"
    GOOGLE_YOUTUBE = "google_youtube_1920x1080"
    GOOGLE_SHORTS = "google_shorts_1080x1920"
    GOOGLE_DISCOVERY = "google_discovery_1200x628"


# Format -> (width, height) mapping
FORMAT_DIMENSIONS: dict[ChannelFormat, tuple[int, int]] = {
    ChannelFormat.NAVER_SHOPPING_SQUARE: (1000, 1000),
    ChannelFormat.NAVER_BRAND_BANNER_PC: (750, 200),
    ChannelFormat.NAVER_BRAND_BANNER_MOBILE: (640, 300),
    ChannelFormat.NAVER_DISPLAY: (1200, 628),
    ChannelFormat.NAVER_NATIVE: (500, 500),
    ChannelFormat.KAKAO_DISPLAY: (1200, 628),
    ChannelFormat.KAKAO_NATIVE: (500, 500),
    ChannelFormat.KAKAO_BIZBOARD: (1029, 258),
    ChannelFormat.KAKAO_MESSAGE: (800, 400),
    ChannelFormat.KAKAO_VIDEO_LANDSCAPE: (1920, 1080),
    ChannelFormat.KAKAO_VIDEO_SQUARE: (1080, 1080),
    ChannelFormat.KAKAO_VIDEO_VERTICAL: (1080, 1920),
    ChannelFormat.META_FEED_SQUARE: (1080, 1080),
    ChannelFormat.META_FEED_PORTRAIT: (1080, 1350),
    ChannelFormat.META_LINK: (1200, 628),
    ChannelFormat.META_REELS: (1080, 1920),
    ChannelFormat.META_CAROUSEL: (1080, 1080),
    ChannelFormat.GOOGLE_DISPLAY: (1200, 628),
    ChannelFormat.GOOGLE_SQUARE: (1200, 1200),
    ChannelFormat.GOOGLE_YOUTUBE: (1920, 1080),
    ChannelFormat.GOOGLE_SHORTS: (1080, 1920),
    ChannelFormat.GOOGLE_DISCOVERY: (1200, 628),
}

# Channel -> default formats mapping
CHANNEL_DEFAULT_FORMATS: dict[str, list[ChannelFormat]] = {
    "naver": [
        ChannelFormat.NAVER_SHOPPING_SQUARE,
        ChannelFormat.NAVER_DISPLAY,
    ],
    "kakao": [
        ChannelFormat.KAKAO_DISPLAY,
        ChannelFormat.KAKAO_NATIVE,
        ChannelFormat.KAKAO_BIZBOARD,
    ],
    "meta": [
        ChannelFormat.META_FEED_SQUARE,
        ChannelFormat.META_FEED_PORTRAIT,
        ChannelFormat.META_LINK,
    ],
    "google": [
        ChannelFormat.GOOGLE_DISPLAY,
        ChannelFormat.GOOGLE_SQUARE,
    ],
}


class VisualBrief(BaseModel):
    """AI-generated visual brief for image generation."""

    image_prompt_en: str = Field(..., description="English prompt for Flux 2.0 Pro")
    style: str = Field(default="photorealistic", description="Visual style")
    mood: str = Field(default="professional", description="Visual mood/tone")
    color_palette: list[str] = Field(default_factory=list)
    brand_elements: list[str] = Field(default_factory=list)
    negative_prompt: Optional[str] = None


class TextOverlay(BaseModel):
    """Korean text overlay spec for Creatomate."""

    headline_ko: str = Field(..., description="Korean headline text")
    subtext_ko: Optional[str] = Field(None, description="Korean subtext")
    cta_ko: Optional[str] = Field(None, description="Korean CTA text")
    logo_url: Optional[str] = None
    font_family: str = "Pretendard"
    headline_color: str = "#FFFFFF"
    headline_size: int = 48
    background_opacity: float = 0.3


class VisualAsset(BaseModel):
    """A single visual asset (image, video, or composite)."""

    id: str = Field(default_factory=lambda: f"vis_{uuid4().hex[:12]}")
    campaign_id: str
    creative_id: Optional[str] = None
    channel: str
    format: ChannelFormat
    asset_type: AssetType = AssetType.IMAGE
    status: VisualStatus = VisualStatus.PENDING
    # Paths
    raw_image_path: Optional[str] = None  # AI-generated image (no text)
    composite_path: Optional[str] = None  # Final with Korean overlay
    # Generation details
    visual_brief: Optional[dict] = None
    text_overlay: Optional[dict] = None
    # Review
    review_feedback: Optional[str] = None
    canva_edit_url: Optional[str] = None
    # Cost tracking
    generation_cost_usd: float = 0.0
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class VisualGenerationRequest(BaseModel):
    """Request to generate visuals for a campaign."""

    campaign_id: str
    channels: list[str] = Field(default_factory=lambda: ["naver", "meta", "google", "kakao"])
    formats: Optional[list[ChannelFormat]] = None  # None = use channel defaults
    product_description: str
    target_audience: str
    brand_name: Optional[str] = None
    logo_url: Optional[str] = None
    headline_ko: str = Field(..., description="Korean headline for overlay")
    subtext_ko: Optional[str] = None
    cta_ko: Optional[str] = None
    style_preference: str = "photorealistic"
    include_video: bool = False
    include_avatar: bool = False


class VisualGenerationResponse(BaseModel):
    """Response from visual generation."""

    campaign_id: str
    assets: list[VisualAsset]
    total_cost_usd: float
    generation_time_seconds: float
    skipped_formats: list[str] = Field(default_factory=list)


class VisualReviewRequest(BaseModel):
    """Review request for a visual asset."""

    action: str = Field(..., description="approve | reject | edit")
    feedback: Optional[str] = None


class VisualReviewResponse(BaseModel):
    """Response from visual review."""

    asset_id: str
    new_status: VisualStatus
    canva_edit_url: Optional[str] = None
    message: str
