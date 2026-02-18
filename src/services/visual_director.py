"""VISUAL_DIRECTOR — orchestrates the full visual generation pipeline.

Flow:
1. Claude generates visual brief (English prompt + style + mood)
2. For each channel x format (parallel):
   a. Flux 2.0 Pro -> AI image (no Korean text)
   b. AssetStorage -> save raw
   c. Creatomate -> Korean text overlay
   d. AssetStorage -> save composite
3. Optional: Runway video, HeyGen avatar
4. All assets -> DRAFT status -> ready for review
"""

import asyncio
import time
from typing import Any, Optional

import anthropic
import structlog

from src.config.settings import Settings
from src.models.visual import (
    CHANNEL_DEFAULT_FORMATS,
    AssetType,
    ChannelFormat,
    TextOverlay,
    VisualAsset,
    VisualBrief,
    VisualGenerationRequest,
    VisualGenerationResponse,
    VisualStatus,
)
from src.services.asset_storage import AssetStorage
from src.services.compositor import Compositor
from src.services.image_generator import ImageGenerator
from src.storage.repositories import VisualAssetRepository

logger = structlog.get_logger()

VISUAL_BRIEF_PROMPT = """You are a visual director for Korean digital advertising.

Given a product/campaign brief, generate an IMAGE PROMPT in English for AI image generation.

CRITICAL RULES:
- The prompt is for Flux 2.0 Pro (text-to-image AI)
- Write the prompt in ENGLISH only
- Do NOT include any Korean/CJK text in the prompt
- Do NOT include any text overlay instructions (text will be added separately)
- Focus on visual composition, mood, lighting, colors, product placement
- The image should work as a background for Korean text overlay

Output JSON:
{
  "image_prompt_en": "detailed English prompt for image generation",
  "style": "photorealistic | illustration | 3d_render | flat_design | minimal",
  "mood": "professional | energetic | warm | luxurious | playful | calm",
  "color_palette": ["#hex1", "#hex2", "#hex3"],
  "negative_prompt": "things to avoid in the image"
}"""


class VisualDirectorService:
    """Orchestrates visual asset generation for campaigns."""

    def __init__(
        self,
        settings: Settings,
        visual_repo: VisualAssetRepository,
        asset_storage: AssetStorage,
    ) -> None:
        self._settings = settings
        self._repo = visual_repo
        self._storage = asset_storage

        # AI client for brief generation
        self._ai_client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self._ai_model = settings.ai_model

        # External services (lazy init)
        self._image_gen: Optional[ImageGenerator] = None
        self._compositor: Optional[Compositor] = None
        # Optional services
        self._video_gen = None  # Runway — Sprint 4
        self._avatar_gen = None  # HeyGen — Sprint 4
        self._canva = None  # Canva — Sprint 4

    def _get_image_gen(self) -> ImageGenerator:
        if self._image_gen is None:
            if not self._settings.fal_api_key:
                raise RuntimeError("FAL_API_KEY not configured")
            self._image_gen = ImageGenerator(self._settings.fal_api_key)
        return self._image_gen

    def _get_compositor(self) -> Compositor:
        if self._compositor is None:
            if not self._settings.creatomate_api_key:
                raise RuntimeError("CREATOMATE_API_KEY not configured")
            self._compositor = Compositor(self._settings.creatomate_api_key)
        return self._compositor

    async def generate_visuals(
        self, request: VisualGenerationRequest
    ) -> VisualGenerationResponse:
        """Full visual generation pipeline."""
        start_time = time.time()
        total_cost = 0.0
        assets: list[VisualAsset] = []
        skipped: list[str] = []

        # 1. Determine formats per channel
        format_list = self._resolve_formats(request.channels, request.formats)

        # 2. Generate visual brief via Claude
        brief = await self._generate_visual_brief(request)

        # 3. Build text overlay
        overlay = TextOverlay(
            headline_ko=request.headline_ko,
            subtext_ko=request.subtext_ko,
            cta_ko=request.cta_ko,
            logo_url=request.logo_url,
        )

        # 4. Generate images in parallel (channel x format)
        tasks = []
        for channel, fmt in format_list:
            tasks.append(
                self._generate_single_asset(
                    request.campaign_id, channel, fmt, brief, overlay
                )
            )

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for i, result in enumerate(results):
            channel, fmt = format_list[i]
            if isinstance(result, Exception):
                logger.error(
                    "visual_generation_failed",
                    channel=channel,
                    format=fmt.value,
                    error=str(result),
                )
                skipped.append(f"{channel}/{fmt.value}: {result}")
            else:
                asset, cost = result
                total_cost += cost
                assets.append(asset)

        elapsed = time.time() - start_time
        logger.info(
            "visual_generation_complete",
            campaign_id=request.campaign_id,
            total_assets=len(assets),
            skipped=len(skipped),
            total_cost=total_cost,
            elapsed_seconds=round(elapsed, 1),
        )

        return VisualGenerationResponse(
            campaign_id=request.campaign_id,
            assets=assets,
            total_cost_usd=round(total_cost, 4),
            generation_time_seconds=round(elapsed, 1),
            skipped_formats=skipped,
        )

    async def _generate_visual_brief(
        self, request: VisualGenerationRequest
    ) -> VisualBrief:
        """Use Claude to generate an English image prompt."""
        user_msg = (
            f"Product: {request.product_description}\n"
            f"Target audience: {request.target_audience}\n"
            f"Brand: {request.brand_name or 'N/A'}\n"
            f"Style preference: {request.style_preference}\n"
            f"Korean headline: {request.headline_ko}\n"
            f"Korean CTA: {request.cta_ko or 'N/A'}\n\n"
            "Generate a visual brief for this ad campaign."
        )

        response = self._ai_client.messages.create(
            model=self._ai_model,
            max_tokens=1024,
            system=VISUAL_BRIEF_PROMPT,
            messages=[{"role": "user", "content": user_msg}],
        )
        result_text = response.content[0].text

        # Parse JSON from response
        import json
        try:
            # Handle markdown code blocks
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0]
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0]
            data = json.loads(result_text.strip())
        except (json.JSONDecodeError, IndexError):
            # Fallback: use product description as prompt
            logger.warning("visual_brief_parse_failed", raw=result_text[:200])
            data = {
                "image_prompt_en": (
                    f"Professional advertising photo for {request.product_description}, "
                    f"clean modern style, high quality product photography, "
                    f"suitable for digital advertising"
                ),
                "style": request.style_preference,
                "mood": "professional",
                "color_palette": [],
                "negative_prompt": "text, watermark, logo, words, letters, blurry",
            }

        return VisualBrief(**data)

    async def _generate_single_asset(
        self,
        campaign_id: str,
        channel: str,
        fmt: ChannelFormat,
        brief: VisualBrief,
        overlay: TextOverlay,
    ) -> tuple[VisualAsset, float]:
        """Generate a single visual asset: AI image -> Korean overlay -> save."""
        cost = 0.0
        image_gen = self._get_image_gen()
        compositor = self._get_compositor()

        # Create asset record
        asset = VisualAsset(
            campaign_id=campaign_id,
            channel=channel,
            format=fmt,
            asset_type=AssetType.IMAGE,
            status=VisualStatus.GENERATING,
            visual_brief=brief.model_dump(),
            text_overlay=overlay.model_dump(),
        )
        await self._repo.create(asset)

        try:
            # Step 1: Generate AI image
            image_url, gen_cost = await image_gen.generate(brief, fmt)
            cost += gen_cost

            # Step 2: Download and save raw image
            raw_bytes = await image_gen.download_image(image_url)
            raw_path = await self._storage.save_raw_image(
                campaign_id, asset.id, raw_bytes
            )

            # Step 3: Composite with Korean text
            await self._repo.update_status(
                asset.id, VisualStatus.COMPOSITING, raw_image_path=raw_path
            )
            composite_url, comp_cost = await compositor.composite(
                image_url, overlay, fmt
            )
            cost += comp_cost

            # Step 4: Download and save composite
            comp_bytes = await compositor.download_render(composite_url)
            comp_path = await self._storage.save_composite(
                campaign_id, asset.id, comp_bytes
            )

            # Step 5: Update to DRAFT
            updated = await self._repo.update_status(
                asset.id,
                VisualStatus.DRAFT,
                composite_path=comp_path,
                generation_cost_usd=cost,
            )
            if updated:
                asset = updated

            logger.info(
                "single_asset_done",
                asset_id=asset.id,
                channel=channel,
                format=fmt.value,
                cost=cost,
            )
            return asset, cost

        except Exception as e:
            await self._repo.update_status(asset.id, VisualStatus.FAILED)
            raise

    def _resolve_formats(
        self,
        channels: list[str],
        explicit_formats: Optional[list[ChannelFormat]],
    ) -> list[tuple[str, ChannelFormat]]:
        """Build list of (channel, format) pairs to generate."""
        if explicit_formats:
            # Map explicit formats to their channels
            result = []
            for fmt in explicit_formats:
                channel = fmt.value.split("_")[0]
                result.append((channel, fmt))
            return result

        # Use channel defaults
        result = []
        for channel in channels:
            for fmt in CHANNEL_DEFAULT_FORMATS.get(channel, []):
                result.append((channel, fmt))
        return result

    async def review_asset(
        self, asset_id: str, action: str, feedback: Optional[str] = None
    ) -> VisualAsset:
        """Review a visual asset: approve, reject, or send to edit."""
        asset = await self._repo.get(asset_id)
        if not asset:
            raise ValueError(f"Asset {asset_id} not found")

        if action == "approve":
            updated = await self._repo.update_status(asset_id, VisualStatus.APPROVED)
        elif action == "reject":
            updated = await self._repo.update_status(
                asset_id, VisualStatus.REJECTED, review_feedback=feedback
            )
        elif action == "edit":
            # Generate Canva edit URL (Sprint 4)
            updated = await self._repo.update_status(
                asset_id, VisualStatus.EDITING, review_feedback=feedback
            )
        else:
            raise ValueError(f"Invalid action: {action}")

        return updated or asset

    async def regenerate_asset(
        self, asset_id: str, request: VisualGenerationRequest
    ) -> VisualAsset:
        """Regenerate a rejected asset with updated parameters."""
        old_asset = await self._repo.get(asset_id)
        if not old_asset:
            raise ValueError(f"Asset {asset_id} not found")

        brief = await self._generate_visual_brief(request)
        overlay = TextOverlay(
            headline_ko=request.headline_ko,
            subtext_ko=request.subtext_ko,
            cta_ko=request.cta_ko,
            logo_url=request.logo_url,
        )

        new_asset, _ = await self._generate_single_asset(
            old_asset.campaign_id,
            old_asset.channel,
            old_asset.format,
            brief,
            overlay,
        )
        return new_asset

    async def get_campaign_assets(
        self, campaign_id: str, status: Optional[str] = None
    ) -> list[VisualAsset]:
        return await self._repo.list_by_campaign(campaign_id, status)

    async def close(self) -> None:
        """Clean up HTTP clients."""
        if self._image_gen:
            await self._image_gen.close()
        if self._compositor:
            await self._compositor.close()
