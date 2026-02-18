"""Image generation via Flux 2.0 Pro on fal.ai."""

import asyncio

import structlog

from src.models.visual import ChannelFormat, FORMAT_DIMENSIONS, VisualBrief
from src.services.base import ExternalAPIService

logger = structlog.get_logger()

FAL_BASE_URL = "https://queue.fal.run"
FLUX_MODEL = "fal-ai/flux-pro/v1.1-ultra"
COST_PER_IMAGE = 0.05  # ~$0.05 per image


class ImageGenerator(ExternalAPIService):
    """Generate images using Flux 2.0 Pro via fal.ai queue API."""

    def __init__(self, api_key: str) -> None:
        super().__init__(api_key=api_key, base_url=FAL_BASE_URL, timeout=180.0)

    def _default_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Key {self._api_key}",
            "Content-Type": "application/json",
        }

    async def generate(
        self,
        brief: VisualBrief,
        fmt: ChannelFormat,
    ) -> tuple[str, float]:
        """Generate an image. Returns (image_url, cost_usd).

        Uses fal.ai queue: submit -> poll until done -> get result.
        """
        width, height = FORMAT_DIMENSIONS[fmt]

        payload = {
            "prompt": brief.image_prompt_en,
            "image_size": {"width": width, "height": height},
            "num_images": 1,
            "safety_tolerance": "2",
            "output_format": "png",
        }
        if brief.negative_prompt:
            payload["negative_prompt"] = brief.negative_prompt

        logger.info(
            "flux_generate_start",
            format=fmt.value,
            size=f"{width}x{height}",
            prompt_len=len(brief.image_prompt_en),
        )

        # Submit to queue
        submit_resp = await self._post(f"/{FLUX_MODEL}", json=payload)

        # fal.ai returns the result directly for sync, or request_id for queue
        if "images" in submit_resp:
            # Direct result
            image_url = submit_resp["images"][0]["url"]
        elif "request_id" in submit_resp:
            # Queue mode — poll for result
            request_id = submit_resp["request_id"]
            image_url = await self._poll_result(request_id)
        else:
            raise RuntimeError(f"Unexpected fal.ai response: {submit_resp}")

        logger.info("flux_generate_done", format=fmt.value, url=image_url[:80])
        return image_url, COST_PER_IMAGE

    async def _poll_result(self, request_id: str, max_wait: int = 120) -> str:
        """Poll fal.ai queue until result is ready."""
        status_url = f"/{FLUX_MODEL}/requests/{request_id}/status"
        for _ in range(max_wait // 2):
            resp = await self._get(status_url)
            status = resp.get("status")
            if status == "COMPLETED":
                result_url = f"/{FLUX_MODEL}/requests/{request_id}"
                result = await self._get(result_url)
                return result["images"][0]["url"]
            if status in ("FAILED", "CANCELLED"):
                raise RuntimeError(f"fal.ai request {request_id} {status}")
            await asyncio.sleep(2)
        raise TimeoutError(f"fal.ai request {request_id} timed out after {max_wait}s")

    async def download_image(self, url: str) -> bytes:
        """Download generated image bytes."""
        return await self._download(url)
