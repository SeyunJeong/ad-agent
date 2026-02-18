"""Video generation via Runway Gen-4 (submit-poll pattern)."""

import asyncio

import structlog

from src.services.base import ExternalAPIService

logger = structlog.get_logger()

RUNWAY_BASE_URL = "https://api.dev.runwayml.com/v1"
COST_PER_5SEC = 0.50


class VideoGenerator(ExternalAPIService):
    """Generate short videos using Runway Gen-4."""

    def __init__(self, api_key: str) -> None:
        super().__init__(api_key=api_key, base_url=RUNWAY_BASE_URL, timeout=300.0)

    def _default_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
            "X-Runway-Version": "2024-11-06",
        }

    async def generate_from_image(
        self,
        image_url: str,
        prompt: str = "",
        duration: int = 5,
    ) -> tuple[str, float]:
        """Generate video from a still image. Returns (video_url, cost_usd).

        Uses Runway's image-to-video (submit -> poll) pattern.
        """
        payload = {
            "model": "gen4_turbo",
            "promptImage": image_url,
            "duration": duration,
            "ratio": "16:9",
        }
        if prompt:
            payload["promptText"] = prompt

        logger.info("runway_generate_start", duration=duration)

        # Submit task
        resp = await self._post("/image_to_video", json=payload)
        task_id = resp.get("id")
        if not task_id:
            raise RuntimeError(f"Runway submit failed: {resp}")

        # Poll for result
        video_url = await self._poll_task(task_id)
        cost = COST_PER_5SEC * (duration / 5)

        logger.info("runway_generate_done", task_id=task_id, cost=cost)
        return video_url, cost

    async def generate_from_text(
        self,
        prompt: str,
        duration: int = 5,
    ) -> tuple[str, float]:
        """Generate video from text prompt only."""
        payload = {
            "model": "gen4_turbo",
            "promptText": prompt,
            "duration": duration,
            "ratio": "16:9",
        }

        resp = await self._post("/text_to_video", json=payload)
        task_id = resp.get("id")
        if not task_id:
            raise RuntimeError(f"Runway submit failed: {resp}")

        video_url = await self._poll_task(task_id)
        cost = COST_PER_5SEC * (duration / 5)
        return video_url, cost

    async def _poll_task(self, task_id: str, max_wait: int = 240) -> str:
        """Poll Runway task until complete."""
        for _ in range(max_wait // 5):
            resp = await self._get(f"/tasks/{task_id}")
            status = resp.get("status")

            if status == "SUCCEEDED":
                output = resp.get("output", [])
                if output:
                    return output[0]
                raise RuntimeError(f"Runway task {task_id} succeeded but no output")

            if status in ("FAILED", "CANCELLED"):
                failure = resp.get("failure")
                raise RuntimeError(f"Runway task {task_id} {status}: {failure}")

            await asyncio.sleep(5)

        raise TimeoutError(f"Runway task {task_id} timed out after {max_wait}s")

    async def download_video(self, url: str) -> bytes:
        return await self._download(url)
