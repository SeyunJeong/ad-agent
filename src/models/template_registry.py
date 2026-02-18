"""Creatomate template registry — maps channel formats to template IDs.

Templates must be created in the Creatomate dashboard first.
Each template receives: background_image, headline, subtext, cta, logo.
"""

from src.models.visual import ChannelFormat


# Creatomate template IDs — configure in dashboard, map here.
# Set to None for formats without a template yet.
CREATOMATE_TEMPLATES: dict[ChannelFormat, str | None] = {
    # Naver
    ChannelFormat.NAVER_SHOPPING_SQUARE: None,
    ChannelFormat.NAVER_BRAND_BANNER_PC: None,
    ChannelFormat.NAVER_BRAND_BANNER_MOBILE: None,
    ChannelFormat.NAVER_DISPLAY: None,
    ChannelFormat.NAVER_NATIVE: None,
    # Kakao
    ChannelFormat.KAKAO_DISPLAY: None,
    ChannelFormat.KAKAO_NATIVE: None,
    ChannelFormat.KAKAO_BIZBOARD: None,
    ChannelFormat.KAKAO_MESSAGE: None,
    ChannelFormat.KAKAO_VIDEO_LANDSCAPE: None,
    ChannelFormat.KAKAO_VIDEO_SQUARE: None,
    ChannelFormat.KAKAO_VIDEO_VERTICAL: None,
    # Meta
    ChannelFormat.META_FEED_SQUARE: None,
    ChannelFormat.META_FEED_PORTRAIT: None,
    ChannelFormat.META_LINK: None,
    ChannelFormat.META_REELS: None,
    ChannelFormat.META_CAROUSEL: None,
    # Google
    ChannelFormat.GOOGLE_DISPLAY: None,
    ChannelFormat.GOOGLE_SQUARE: None,
    ChannelFormat.GOOGLE_YOUTUBE: None,
    ChannelFormat.GOOGLE_SHORTS: None,
    ChannelFormat.GOOGLE_DISCOVERY: None,
}


def get_template_id(fmt: ChannelFormat) -> str | None:
    """Get Creatomate template ID for a format. None = not configured."""
    return CREATOMATE_TEMPLATES.get(fmt)


def has_template(fmt: ChannelFormat) -> bool:
    """Check if a Creatomate template exists for this format."""
    return CREATOMATE_TEMPLATES.get(fmt) is not None


def set_template_id(fmt: ChannelFormat, template_id: str) -> None:
    """Register a Creatomate template ID for a format (runtime override)."""
    CREATOMATE_TEMPLATES[fmt] = template_id


def list_configured_templates() -> dict[str, str]:
    """Return all formats that have templates configured."""
    return {
        fmt.value: tid
        for fmt, tid in CREATOMATE_TEMPLATES.items()
        if tid is not None
    }
