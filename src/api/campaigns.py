"""Campaign management API endpoints."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.api.deps import CampaignRepo, Channels, Orchestrator
from src.models.campaign import (
    Campaign,
    CampaignBrief,
    CampaignConfig,
    CampaignFilters,
    CampaignStatus,
)

router = APIRouter(prefix="/campaigns", tags=["campaigns"])


class ApiResponse(BaseModel):
    status: str = "success"
    data: dict | list | None = None
    message: str | None = None


# POST /campaigns — 새 캠페인 생성
@router.post("", response_model=ApiResponse)
async def create_campaign(
    brief: CampaignBrief,
    repo: CampaignRepo,
    orchestrator: Orchestrator,
) -> ApiResponse:
    """새 캠페인을 생성하고 AI 전략 수립을 시작합니다."""
    config = CampaignConfig(
        name=f"{brief.business_name}_{brief.objective.value}",
        brief=brief,
    )
    campaign = Campaign(config=config, status=CampaignStatus.PLANNING)

    # Save to DB
    await repo.create(campaign)

    # Run AI pipeline
    plan = await orchestrator.create_campaign_plan(brief, campaign.id)

    # Update with strategy
    campaign.strategy_summary = plan["strategy"]["strategy"]
    campaign.status = CampaignStatus.READY
    await repo.update(campaign)

    return ApiResponse(
        data={
            "campaign_id": campaign.id,
            "status": campaign.status.value,
            "strategy": plan["strategy"]["strategy"][:500],
            "channels": plan["channels"],
        },
        message="캠페인 플랜이 생성되었습니다",
    )


# GET /campaigns — 캠페인 목록
@router.get("", response_model=ApiResponse)
async def list_campaigns(
    repo: CampaignRepo,
    status: str | None = None,
    channel: str | None = None,
) -> ApiResponse:
    filters = CampaignFilters(
        status=CampaignStatus(status) if status else None,
        channel=channel,
    )
    campaigns = await repo.list(filters)
    return ApiResponse(
        data=[
            {
                "id": c.id,
                "name": c.config.name,
                "status": c.status.value,
                "budget": c.config.brief.budget.total_amount,
                "channels": [a.channel for a in c.config.channel_allocations],
                "created_at": c.created_at.isoformat(),
            }
            for c in campaigns
        ]
    )


# GET /campaigns/{id} — 캠페인 상세
@router.get("/{campaign_id}", response_model=ApiResponse)
async def get_campaign(campaign_id: str, repo: CampaignRepo) -> ApiResponse:
    campaign = await repo.get(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="캠페인을 찾을 수 없습니다")
    return ApiResponse(data=campaign.model_dump(mode="json"))


# PUT /campaigns/{id} — 캠페인 수정
@router.put("/{campaign_id}", response_model=ApiResponse)
async def update_campaign(
    campaign_id: str,
    updates: dict,
    repo: CampaignRepo,
) -> ApiResponse:
    campaign = await repo.get(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="캠페인을 찾을 수 없습니다")

    if "name" in updates:
        campaign.config.name = updates["name"]
    if "status" in updates:
        campaign.status = CampaignStatus(updates["status"])

    await repo.update(campaign)
    return ApiResponse(data={"id": campaign_id, "updated": True})


# DELETE /campaigns/{id}
@router.delete("/{campaign_id}", response_model=ApiResponse)
async def delete_campaign(campaign_id: str, repo: CampaignRepo) -> ApiResponse:
    await repo.delete(campaign_id)
    return ApiResponse(message="캠페인이 보관처리 되었습니다")


# POST /campaigns/{id}/launch — 캠페인 론칭
@router.post("/{campaign_id}/launch", response_model=ApiResponse)
async def launch_campaign(
    campaign_id: str,
    repo: CampaignRepo,
    channels: Channels,
) -> ApiResponse:
    """캠페인을 각 채널에 실제로 생성하고 활성화합니다."""
    campaign = await repo.get(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="캠페인을 찾을 수 없습니다")

    if campaign.status not in (CampaignStatus.READY, CampaignStatus.PAUSED):
        raise HTTPException(
            status_code=400,
            detail=f"론칭할 수 없는 상태입니다: {campaign.status.value}",
        )

    # Launch on each configured channel
    results = {}
    for alloc in campaign.config.channel_allocations:
        adapter = channels.get(alloc.channel)
        if not await adapter.is_configured():
            results[alloc.channel] = {"error": f"{alloc.channel} 채널 미설정"}
            continue

        try:
            result = await adapter.create_campaign(campaign.config)
            channel_id = result.get("id") or result.get("nccCampaignId", "")
            campaign.channel_campaign_ids[alloc.channel] = channel_id
            results[alloc.channel] = {"status": "launched", "channel_id": channel_id}
        except Exception as e:
            results[alloc.channel] = {"error": str(e)}

    campaign.status = CampaignStatus.ACTIVE
    await repo.update(campaign)

    return ApiResponse(
        data={"campaign_id": campaign_id, "channel_results": results},
        message="캠페인이 론칭되었습니다",
    )


# POST /campaigns/{id}/pause
@router.post("/{campaign_id}/pause", response_model=ApiResponse)
async def pause_campaign(
    campaign_id: str,
    repo: CampaignRepo,
    channels: Channels,
) -> ApiResponse:
    campaign = await repo.get(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="캠페인을 찾을 수 없습니다")

    for ch, ch_id in campaign.channel_campaign_ids.items():
        adapter = channels.get(ch)
        try:
            await adapter.pause_campaign(ch_id)
        except Exception:
            pass

    campaign.status = CampaignStatus.PAUSED
    await repo.update(campaign)
    return ApiResponse(message="캠페인이 일시 중지되었습니다")


# POST /campaigns/{id}/resume
@router.post("/{campaign_id}/resume", response_model=ApiResponse)
async def resume_campaign(
    campaign_id: str,
    repo: CampaignRepo,
    channels: Channels,
) -> ApiResponse:
    campaign = await repo.get(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="캠페인을 찾을 수 없습니다")

    for ch, ch_id in campaign.channel_campaign_ids.items():
        adapter = channels.get(ch)
        try:
            await adapter.resume_campaign(ch_id)
        except Exception:
            pass

    campaign.status = CampaignStatus.ACTIVE
    await repo.update(campaign)
    return ApiResponse(message="캠페인이 재개되었습니다")
