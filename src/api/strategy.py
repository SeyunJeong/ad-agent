"""Strategy and research API endpoints."""

from fastapi import APIRouter
from pydantic import BaseModel

from src.api.deps import CampaignRepo, Orchestrator
from src.models.campaign import CampaignBrief

router = APIRouter(prefix="/strategy", tags=["strategy"])


class ApiResponse(BaseModel):
    status: str = "success"
    data: dict | list | None = None
    message: str | None = None


# POST /strategy/generate — AI 전략 수립 (self-debate)
@router.post("/generate", response_model=ApiResponse)
async def generate_strategy(
    brief: CampaignBrief,
    orchestrator: Orchestrator,
) -> ApiResponse:
    result = await orchestrator.generate_strategy(brief)
    return ApiResponse(
        data={
            "strategy": result["strategy"],
            "blue_team": result["blue_team"][:1000],
            "red_team": result["red_team"][:1000],
            "process": result["process"],
        },
        message="전략이 수립되었습니다 (Self-Debate 완료)",
    )


# POST /strategy/channel-mix — 채널 믹스 추천
@router.post("/channel-mix", response_model=ApiResponse)
async def recommend_channel_mix(
    brief: CampaignBrief,
    orchestrator: Orchestrator,
) -> ApiResponse:
    result = await orchestrator.generate_strategy(brief)
    return ApiResponse(
        data={"channel_mix": result["strategy"]},
        message="채널 믹스가 추천되었습니다",
    )


# POST /strategy/budget-allocation — 예산 배분 추천
@router.post("/budget-allocation", response_model=ApiResponse)
async def recommend_budget(
    brief: CampaignBrief,
    orchestrator: Orchestrator,
) -> ApiResponse:
    bid_result = await orchestrator.optimize_bids(
        campaign_id="new",
        performance_data={},
        current_config={"brief": brief.model_dump()},
    )
    return ApiResponse(
        data={"budget_allocation": bid_result},
        message="예산 배분이 추천되었습니다",
    )
