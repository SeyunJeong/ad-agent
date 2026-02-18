"""Base class for external API services."""

import httpx
import structlog

logger = structlog.get_logger()


class ExternalAPIService:
    """Base for all external API integrations (fal.ai, Creatomate, etc.)."""

    def __init__(self, api_key: str, base_url: str, timeout: float = 120.0) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self._base_url,
                timeout=self._timeout,
                headers=self._default_headers(),
            )
        return self._client

    def _default_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Key {self._api_key}",
            "Content-Type": "application/json",
        }

    async def _post(self, path: str, json: dict, **kwargs) -> dict:
        client = await self._get_client()
        resp = await client.post(path, json=json, **kwargs)
        resp.raise_for_status()
        return resp.json()

    async def _get(self, path: str, **kwargs) -> dict:
        client = await self._get_client()
        resp = await client.get(path, **kwargs)
        resp.raise_for_status()
        return resp.json()

    async def _download(self, url: str) -> bytes:
        """Download binary content from a URL."""
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            return resp.content

    async def close(self) -> None:
        if self._client and not self._client.is_closed:
            await self._client.close()
