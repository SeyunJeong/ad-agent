"""Local file storage for visual assets."""

import os
from pathlib import Path

import structlog

logger = structlog.get_logger()

ASSETS_ROOT = Path("data/assets")


class AssetStorage:
    """Store and serve visual assets on local filesystem."""

    def __init__(self, root: Path = ASSETS_ROOT) -> None:
        self._root = root
        self._root.mkdir(parents=True, exist_ok=True)

    def _campaign_dir(self, campaign_id: str, subdir: str = "") -> Path:
        path = self._root / campaign_id
        if subdir:
            path = path / subdir
        path.mkdir(parents=True, exist_ok=True)
        return path

    async def save_raw_image(
        self, campaign_id: str, asset_id: str, data: bytes, ext: str = "png"
    ) -> str:
        """Save AI-generated raw image (no text). Returns relative path."""
        dir_ = self._campaign_dir(campaign_id, "raw")
        filename = f"{asset_id}.{ext}"
        filepath = dir_ / filename
        filepath.write_bytes(data)
        rel = filepath.relative_to(self._root)
        logger.info("asset_saved", type="raw", path=str(rel), size=len(data))
        return str(rel)

    async def save_composite(
        self, campaign_id: str, asset_id: str, data: bytes, ext: str = "png"
    ) -> str:
        """Save composited image (with Korean overlay). Returns relative path."""
        dir_ = self._campaign_dir(campaign_id, "composites")
        filename = f"{asset_id}.{ext}"
        filepath = dir_ / filename
        filepath.write_bytes(data)
        rel = filepath.relative_to(self._root)
        logger.info("asset_saved", type="composite", path=str(rel), size=len(data))
        return str(rel)

    async def save_video(
        self, campaign_id: str, asset_id: str, data: bytes, ext: str = "mp4"
    ) -> str:
        """Save video asset. Returns relative path."""
        dir_ = self._campaign_dir(campaign_id, "videos")
        filename = f"{asset_id}.{ext}"
        filepath = dir_ / filename
        filepath.write_bytes(data)
        rel = filepath.relative_to(self._root)
        logger.info("asset_saved", type="video", path=str(rel), size=len(data))
        return str(rel)

    def get_absolute_path(self, relative_path: str) -> Path:
        """Convert relative asset path to absolute path."""
        return self._root / relative_path

    def exists(self, relative_path: str) -> bool:
        return (self._root / relative_path).exists()

    def delete(self, relative_path: str) -> bool:
        path = self._root / relative_path
        if path.exists():
            os.remove(path)
            logger.info("asset_deleted", path=relative_path)
            return True
        return False

    def list_campaign_assets(self, campaign_id: str) -> list[str]:
        """List all asset files for a campaign."""
        campaign_dir = self._root / campaign_id
        if not campaign_dir.exists():
            return []
        return [
            str(f.relative_to(self._root))
            for f in campaign_dir.rglob("*")
            if f.is_file()
        ]
