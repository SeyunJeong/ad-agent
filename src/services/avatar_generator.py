"""Avatar video generation via HeyGen API."""

import asyncio

import structlog

from src.services.base import ExternalAPIService

logger = structlog.get_logger()

HEYGEN_BASE_URL = "https://api.heygen.com"
COST_PER_MINUTE = 1.00


class AvatarGenerator(ExternalAPIService):
    """Generate avatar talking-head videos using HeyGen."""

    def __init__(self, api_key: str) -> None:
        super().__init__(api_key=api_key, base_url=HEYGEN_BASE_URL, timeout=300.0)

    def _default_headers(self) -> dict[str, str]:
        return {
            "X-Api-Key": self._api_key,
            "Content-Type": "application/json",
        }

    async def generate(
        self,
        script_ko: str,
        avatar_id: str = "default",
        voice_id: str = "ko-KR-InJoonNeural",
        background_url: str | None = None,
    ) -> tuple[str, float]:
        """Generate an avatar video with Korean TTS. Returns (video_url, cost_usd).

        Args:
            script_ko: Korean script for TTS
            avatar_id: HeyGen avatar ID (use 'default' for a generic presenter)
            voice_id: Korean voice ID
            background_url: Optional background image/video URL
        """
        video_input = {
            "character": {
                "type": "avatar",
                "avatar_id": avatar_id,
                "avatar_style": "normal",
            },
            "voice": {
                "type": "text",
                "input_text": script_ko,
                "voice_id": voice_id,
            },
        }
        if background_url:
            video_input["background"] = {
                "type": "image",
                "url": background_url,
            }

        payload = {
            "video_inputs": [video_input],
            "dimension": {"width": 1080, "height": 1920},
        }

        logger.info("heygen_generate_start", script_len=len(script_ko))

        resp = await self._post("/v2/video/generate", json=payload)
        video_id = resp.get("data", {}).get("video_id")
        if not video_id:
            raise RuntimeError(f"HeyGen submit failed: {resp}")

        video_url = await self._poll_video(video_id)
        # Estimate cost based on script length (~150 chars/min for Korean)
        est_minutes = max(len(script_ko) / 150, 0.5)
        cost = COST_PER_MINUTE * est_minutes

        logger.info("heygen_generate_done", video_id=video_id, cost=round(cost, 2))
        return video_url, round(cost, 2)

    async def _poll_video(self, video_id: str, max_wait: int = 300) -> str:
        """Poll HeyGen until video is ready."""
        for _ in range(max_wait // 5):
            resp = await self._get(
                f"/v1/video_status.get",
                params={"video_id": video_id},
            )
            data = resp.get("data", {})
            status = data.get("status")

            if status == "completed":
                return data["video_url"]
            if status == "failed":
                raise RuntimeError(f"HeyGen video {video_id} failed: {data.get('error')}")

            await asyncio.sleep(5)

        raise TimeoutError(f"HeyGen video {video_id} timed out after {max_wait}s")

    async def list_avatars(self) -> list[dict]:
        """List available avatars."""
        resp = await self._get("/v2/avatars")
        return resp.get("data", {}).get("avatars", [])

    async def list_voices(self, language: str = "ko") -> list[dict]:
        """List available voices for a language."""
        resp = await self._get("/v2/voices")
        voices = resp.get("data", {}).get("voices", [])
        return [v for v in voices if v.get("language", "").startswith(language)]

    async def download_video(self, url: str) -> bytes:
        return await self._download(url)
