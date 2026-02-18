"""Channel management API endpoints."""

from fastapi import APIRouter
from pydantic import BaseModel

from src.api.deps import Channels

router = APIRouter(prefix="/channels", tags=["channels"])


class ApiResponse(BaseModel):
    status: str = "success"
    data: dict | list | None = None
    message: str | None = None


# GET /channels — 전체 채널 상태
@router.get("", response_model=ApiResponse)
async def list_channels(channels: Channels) -> ApiResponse:
    infos = await channels.get_all_channel_info()
    return ApiResponse(data=infos)


# GET /channels/configured — 설정 완료된 채널만
@router.get("/configured", response_model=ApiResponse)
async def list_configured_channels(channels: Channels) -> ApiResponse:
    configured = await channels.configured_channels()
    return ApiResponse(data=[c.value for c in configured])


# GET /channels/{channel_id}/info
@router.get("/{channel_id}/info", response_model=ApiResponse)
async def get_channel_info(channel_id: str, channels: Channels) -> ApiResponse:
    adapter = channels.get(channel_id)
    info = await adapter.get_channel_info()
    return ApiResponse(data=info.model_dump())


# GET /channels/{channel_id}/campaigns — 채널의 실제 캠페인 목록
@router.get("/{channel_id}/campaigns", response_model=ApiResponse)
async def list_channel_campaigns(channel_id: str, channels: Channels) -> ApiResponse:
    adapter = channels.get(channel_id)
    if not await adapter.is_configured():
        return ApiResponse(
            status="error",
            message=f"{channel_id} 채널이 설정되지 않았습니다",
        )
    campaigns = await adapter.list_campaigns()
    return ApiResponse(data=campaigns)
