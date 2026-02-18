"""Channel adapter registry — manages all channel adapters."""

import structlog

from src.channels.base import ChannelAdapter
from src.channels.google import GoogleAdsAdapter
from src.channels.kakao import KakaoMomentAdapter
from src.channels.meta import MetaAdsAdapter
from src.channels.naver import NaverSearchAdsAdapter
from src.config.settings import Settings
from src.models.channel import ChannelId

logger = structlog.get_logger()


class ChannelRegistry:
    """채널 어댑터 레지스트리.

    설정된 모든 채널 어댑터를 관리하고 조회.
    """

    def __init__(self, settings: Settings) -> None:
        self._adapters: dict[ChannelId, ChannelAdapter] = {}
        self._init_adapters(settings)

    def _init_adapters(self, s: Settings) -> None:
        self._adapters[ChannelId.NAVER] = NaverSearchAdsAdapter(
            api_key=s.naver_api_key,
            secret_key=s.naver_secret_key,
            customer_id=s.naver_customer_id,
        )
        self._adapters[ChannelId.KAKAO] = KakaoMomentAdapter(
            app_key=s.kakao_app_key,
            access_token=s.kakao_access_token,
        )
        self._adapters[ChannelId.META] = MetaAdsAdapter(
            app_id=s.meta_app_id,
            app_secret=s.meta_app_secret,
            access_token=s.meta_access_token,
            ad_account_id=s.meta_ad_account_id,
        )
        self._adapters[ChannelId.GOOGLE] = GoogleAdsAdapter(
            developer_token=s.google_developer_token,
            client_id=s.google_client_id,
            client_secret=s.google_client_secret,
            refresh_token=s.google_refresh_token,
            customer_id=s.google_customer_id,
        )
        logger.info(
            "channel_registry_initialized",
            channels=list(self._adapters.keys()),
        )

    def get(self, channel_id: str | ChannelId) -> ChannelAdapter:
        if isinstance(channel_id, str):
            channel_id = ChannelId(channel_id)
        adapter = self._adapters.get(channel_id)
        if adapter is None:
            raise ValueError(f"Unknown channel: {channel_id}")
        return adapter

    def all(self) -> dict[ChannelId, ChannelAdapter]:
        return dict(self._adapters)

    async def configured_channels(self) -> list[ChannelId]:
        result = []
        for cid, adapter in self._adapters.items():
            if await adapter.is_configured():
                result.append(cid)
        return result

    async def get_all_channel_info(self) -> list[dict]:
        infos = []
        for adapter in self._adapters.values():
            info = await adapter.get_channel_info()
            infos.append(info.model_dump())
        return infos
