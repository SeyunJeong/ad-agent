"""Creatomate compositor — Korean text overlay on AI-generated images.

This is the KEY service that solves the Korean text rendering problem:
AI generates visuals (English prompt) -> Creatomate adds Korean text overlay.
"""

import asyncio

import structlog

from src.models.template_registry import get_template_id, has_template
from src.models.visual import ChannelFormat, FORMAT_DIMENSIONS, TextOverlay
from src.services.base import ExternalAPIService

logger = structlog.get_logger()

CREATOMATE_BASE_URL = "https://api.creatomate.com/v1"
COST_PER_RENDER = 0.04


class Compositor(ExternalAPIService):
    """Overlay Korean text on AI-generated images via Creatomate."""

    def __init__(self, api_key: str) -> None:
        super().__init__(api_key=api_key, base_url=CREATOMATE_BASE_URL, timeout=120.0)

    def _default_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

    async def composite(
        self,
        background_image_url: str,
        text_overlay: TextOverlay,
        fmt: ChannelFormat,
    ) -> tuple[str, float]:
        """Overlay Korean text on image. Returns (render_url, cost_usd).

        If a Creatomate template is configured for this format, uses template.
        Otherwise, uses dynamic JSON source (no template required).
        """
        template_id = get_template_id(fmt)
        width, height = FORMAT_DIMENSIONS[fmt]

        if template_id:
            return await self._render_with_template(
                template_id, background_image_url, text_overlay
            )
        else:
            return await self._render_dynamic(
                background_image_url, text_overlay, width, height
            )

    async def _render_with_template(
        self,
        template_id: str,
        background_url: str,
        overlay: TextOverlay,
    ) -> tuple[str, float]:
        """Render using a pre-built Creatomate template."""
        modifications = {
            "background": background_url,
            "headline": overlay.headline_ko,
        }
        if overlay.subtext_ko:
            modifications["subtext"] = overlay.subtext_ko
        if overlay.cta_ko:
            modifications["cta"] = overlay.cta_ko
        if overlay.logo_url:
            modifications["logo"] = overlay.logo_url

        payload = {
            "template_id": template_id,
            "modifications": modifications,
        }
        render = await self._start_render(payload)
        url = await self._poll_render(render["id"])
        return url, COST_PER_RENDER

    async def _render_dynamic(
        self,
        background_url: str,
        overlay: TextOverlay,
        width: int,
        height: int,
    ) -> tuple[str, float]:
        """Render using dynamic JSON source (no template needed)."""
        elements = [
            # Background image (fill)
            {
                "type": "image",
                "source": background_url,
                "width": "100%",
                "height": "100%",
                "fit": "cover",
            },
            # Semi-transparent overlay bar at bottom
            {
                "type": "shape",
                "shape": "rectangle",
                "x": "50%",
                "y": "85%",
                "width": "100%",
                "height": "30%",
                "fill_color": f"rgba(0,0,0,{overlay.background_opacity})",
            },
            # Headline
            {
                "type": "text",
                "text": overlay.headline_ko,
                "font_family": overlay.font_family,
                "font_size": self._scale_font(overlay.headline_size, width),
                "font_weight": "700",
                "fill_color": overlay.headline_color,
                "x": "50%",
                "y": "78%",
                "width": "90%",
                "x_alignment": "50%",
                "y_alignment": "50%",
            },
        ]

        if overlay.subtext_ko:
            elements.append({
                "type": "text",
                "text": overlay.subtext_ko,
                "font_family": overlay.font_family,
                "font_size": self._scale_font(overlay.headline_size * 0.6, width),
                "fill_color": overlay.headline_color,
                "x": "50%",
                "y": "88%",
                "width": "85%",
                "x_alignment": "50%",
                "y_alignment": "50%",
            })

        if overlay.cta_ko:
            elements.append({
                "type": "text",
                "text": overlay.cta_ko,
                "font_family": overlay.font_family,
                "font_size": self._scale_font(overlay.headline_size * 0.5, width),
                "font_weight": "700",
                "fill_color": "#FFFFFF",
                "background_color": "#FF6B35",
                "background_border_radius": "8",
                "x": "50%",
                "y": "95%",
                "x_alignment": "50%",
                "y_alignment": "50%",
                "padding": "8",
            })

        if overlay.logo_url:
            elements.append({
                "type": "image",
                "source": overlay.logo_url,
                "x": "8%",
                "y": "8%",
                "width": "15%",
                "x_alignment": "50%",
                "y_alignment": "50%",
            })

        payload = {
            "source": {
                "output_format": "png",
                "width": width,
                "height": height,
                "elements": elements,
            }
        }
        render = await self._start_render(payload)
        url = await self._poll_render(render["id"])
        return url, COST_PER_RENDER

    async def _start_render(self, payload: dict) -> dict:
        """Submit a render job to Creatomate."""
        renders = await self._post("/renders", json=payload)
        # Creatomate returns a list of renders
        if isinstance(renders, list):
            return renders[0]
        return renders

    async def _poll_render(self, render_id: str, max_wait: int = 90) -> str:
        """Poll until render is finished. Returns output URL."""
        for _ in range(max_wait // 2):
            resp = await self._get(f"/renders/{render_id}")
            status = resp.get("status")
            if status == "succeeded":
                return resp["url"]
            if status == "failed":
                raise RuntimeError(
                    f"Creatomate render {render_id} failed: {resp.get('error')}"
                )
            await asyncio.sleep(2)
        raise TimeoutError(f"Creatomate render {render_id} timed out")

    async def download_render(self, url: str) -> bytes:
        """Download rendered composite image."""
        return await self._download(url)

    @staticmethod
    def _scale_font(base_size: float, width: int) -> str:
        """Scale font size relative to image width."""
        # Reference: base_size is for 1080px width
        scaled = int(base_size * (width / 1080))
        return str(max(scaled, 12))
