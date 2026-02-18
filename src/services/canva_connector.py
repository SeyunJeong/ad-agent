"""Canva Connect API — generate edit links for human refinement."""

import structlog

from src.services.base import ExternalAPIService

logger = structlog.get_logger()

CANVA_BASE_URL = "https://api.canva.com/rest/v1"


class CanvaConnector(ExternalAPIService):
    """Create Canva designs from assets for human editing."""

    def __init__(self, api_key: str) -> None:
        super().__init__(api_key=api_key, base_url=CANVA_BASE_URL, timeout=60.0)

    def _default_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

    async def create_design_from_image(
        self,
        image_url: str,
        title: str = "Ad Creative Edit",
        width: int = 1080,
        height: int = 1080,
    ) -> dict[str, str]:
        """Upload image to Canva and create an editable design.

        Returns {"design_id": "...", "edit_url": "..."}.
        """
        # Step 1: Start asset upload job
        upload_resp = await self._post("/asset-uploads", json={
            "name": title,
        })
        upload_url = upload_resp.get("upload_url")
        asset_id = upload_resp.get("id")

        if upload_url:
            # Step 2: Upload the image bytes
            image_data = await self._download(image_url)
            client = await self._get_client()
            await client.put(
                upload_url,
                content=image_data,
                headers={"Content-Type": "image/png"},
            )

        # Step 3: Create design with the uploaded asset
        design_resp = await self._post("/designs", json={
            "design_type": {"type": "custom", "width": width, "height": height},
            "title": title,
        })
        design_id = design_resp.get("design", {}).get("id", "")
        edit_url = design_resp.get("design", {}).get("urls", {}).get("edit_url", "")

        logger.info(
            "canva_design_created",
            design_id=design_id,
            edit_url=edit_url[:60] if edit_url else "N/A",
        )

        return {
            "design_id": design_id,
            "edit_url": edit_url,
            "asset_id": asset_id or "",
        }

    async def get_design_export(self, design_id: str) -> str | None:
        """Export a Canva design as PNG. Returns download URL or None."""
        try:
            resp = await self._post(f"/designs/{design_id}/exports", json={
                "format": {"type": "png"},
            })
            export_id = resp.get("id")
            if not export_id:
                return None

            # Poll for export completion
            import asyncio
            for _ in range(30):
                export = await self._get(f"/exports/{export_id}")
                status = export.get("status")
                if status == "completed":
                    return export.get("urls", [{}])[0].get("url")
                if status == "failed":
                    return None
                await asyncio.sleep(2)

        except Exception as e:
            logger.error("canva_export_failed", error=str(e))

        return None
