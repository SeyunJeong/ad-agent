"""Creative generation API endpoints."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.api.deps import CampaignRepo, Channels, Orchestrator
from src.models.creative import CreativeGenerationRequest

router = APIRouter(prefix="/creative", tags=["creative"])


class ApiResponse(BaseModel):
    status: str = "success"
    data: dict | list | None = None
    message: str | None = None


# POST /creative/generate — AI 광고 카피 생성
@router.post("/generate", response_model=ApiResponse)
async def generate_creatives(
    request: CreativeGenerationRequest,
    repo: CampaignRepo,
    orchestrator: Orchestrator,
) -> ApiResponse:
    campaign = await repo.get(request.campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="캠페인을 찾을 수 없습니다")

    result = await orchestrator.generate_creatives(
        brief=campaign.config.brief,
        channels=request.channels,
        strategy=campaign.strategy_summary or "",
        campaign_id=campaign.id,
    )
    return ApiResponse(
        data={"creatives": result, "campaign_id": request.campaign_id},
        message="광고 카피가 생성되었습니다",
    )


# POST /creative/variations — A/B 변형 생성
@router.post("/variations", response_model=ApiResponse)
async def generate_variations(
    request: CreativeGenerationRequest,
    repo: CampaignRepo,
    orchestrator: Orchestrator,
) -> ApiResponse:
    campaign = await repo.get(request.campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="캠페인을 찾을 수 없습니다")

    result = await orchestrator.generate_creatives(
        brief=campaign.config.brief,
        channels=request.channels,
        strategy=campaign.strategy_summary or "",
        campaign_id=campaign.id,
    )
    return ApiResponse(
        data={"variations": result, "count": request.variations_count},
        message=f"A/B 변형 {request.variations_count}개가 생성되었습니다",
    )


# POST /creative/validate — 소재 유효성 검증
@router.post("/validate", response_model=ApiResponse)
async def validate_creative(
    channel: str,
    headline: str,
    description: str,
    landing_url: str,
    channels_reg: Channels,
) -> ApiResponse:
    from src.models.creative import CreativeConfig

    adapter = channels_reg.get(channel)
    config = CreativeConfig(
        headline=headline,
        description=description,
        landing_url=landing_url,
    )
    result = await adapter.validate_creative(config)
    return ApiResponse(
        data=result.model_dump(),
        message="유효성 검증 완료" if result.is_valid else "유효성 검증 실패",
    )
