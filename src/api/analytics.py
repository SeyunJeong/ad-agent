"""Analytics and reporting API endpoints."""

from datetime import date

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.api.deps import CampaignRepo, Channels, Orchestrator, StatsRepo
from src.models.report import MetricSet, PerformanceQuery

router = APIRouter(prefix="/analytics", tags=["analytics"])


class ApiResponse(BaseModel):
    status: str = "success"
    data: dict | list | None = None
    message: str | None = None


# GET /analytics/dashboard — 전체 대시보드
@router.get("/dashboard", response_model=ApiResponse)
async def get_dashboard(
    campaign_repo: CampaignRepo,
    stats_repo: StatsRepo,
) -> ApiResponse:
    campaigns = await campaign_repo.list()
    total_campaigns = len(campaigns)
    active = sum(1 for c in campaigns if c.status.value == "active")
    total_budget = sum(c.config.brief.budget.total_amount for c in campaigns)

    return ApiResponse(
        data={
            "total_campaigns": total_campaigns,
            "active_campaigns": active,
            "total_budget": total_budget,
            "campaigns": [
                {
                    "id": c.id,
                    "name": c.config.name,
                    "status": c.status.value,
                    "budget": c.config.brief.budget.total_amount,
                }
                for c in campaigns[:10]
            ],
        }
    )


# GET /analytics/campaigns/{id}/performance — 캠페인 성과
@router.get("/campaigns/{campaign_id}/performance", response_model=ApiResponse)
async def get_campaign_performance(
    campaign_id: str,
    start_date: str,
    end_date: str,
    campaign_repo: CampaignRepo,
    stats_repo: StatsRepo,
    channels: Channels,
) -> ApiResponse:
    campaign = await campaign_repo.get(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="캠페인을 찾을 수 없습니다")

    # Try fetching from local DB first
    local_stats = await stats_repo.get_aggregate_stats(campaign_id, start_date, end_date)

    # If no local data, fetch from channels
    if not local_stats or not local_stats.get("impressions"):
        channel_data = {}
        for ch, ch_id in campaign.channel_campaign_ids.items():
            adapter = channels.get(ch)
            try:
                metrics = await adapter.get_performance(ch_id, start_date, end_date)
                channel_data[ch] = metrics.model_dump()

                # Save to local DB
                await stats_repo.save_daily_stats(
                    campaign_id=campaign_id,
                    channel=ch,
                    stat_date=end_date,
                    impressions=metrics.impressions,
                    clicks=metrics.clicks,
                    cost=metrics.cost,
                    conversions=metrics.conversions,
                    revenue=metrics.revenue,
                )
            except Exception as e:
                channel_data[ch] = {"error": str(e)}

        return ApiResponse(data={"campaign_id": campaign_id, "channels": channel_data})

    return ApiResponse(
        data={
            "campaign_id": campaign_id,
            "period": {"start": start_date, "end": end_date},
            "total": local_stats,
        }
    )


# POST /analytics/reports/custom — AI 분석 리포트 생성
@router.post("/reports/custom", response_model=ApiResponse)
async def generate_custom_report(
    query: PerformanceQuery,
    campaign_repo: CampaignRepo,
    stats_repo: StatsRepo,
    orchestrator: Orchestrator,
) -> ApiResponse:
    campaign = await campaign_repo.get(query.campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="캠페인을 찾을 수 없습니다")

    # Gather performance data
    stats = await stats_repo.get_daily_stats(
        query.campaign_id,
        query.start_date.isoformat(),
        query.end_date.isoformat(),
    )
    aggregate = await stats_repo.get_aggregate_stats(
        query.campaign_id,
        query.start_date.isoformat(),
        query.end_date.isoformat(),
    )

    performance_data = {
        "campaign": campaign.config.name,
        "brief": campaign.config.brief.model_dump(),
        "aggregate": aggregate,
        "daily": stats,
    }

    # AI analysis
    report = await orchestrator.analyze_performance(
        campaign_id=query.campaign_id,
        performance_data=performance_data,
        report_type=query.granularity,
    )

    return ApiResponse(
        data={
            "campaign_id": query.campaign_id,
            "report": report,
            "period": {
                "start": query.start_date.isoformat(),
                "end": query.end_date.isoformat(),
            },
        },
        message="분석 리포트가 생성되었습니다",
    )


# POST /analytics/optimization — 최적화 분석
@router.post("/optimization", response_model=ApiResponse)
async def analyze_optimization(
    campaign_id: str,
    campaign_repo: CampaignRepo,
    stats_repo: StatsRepo,
    orchestrator: Orchestrator,
) -> ApiResponse:
    campaign = await campaign_repo.get(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="캠페인을 찾을 수 없습니다")

    today = date.today().isoformat()
    aggregate = await stats_repo.get_aggregate_stats(
        campaign_id, campaign.created_at.date().isoformat(), today
    )

    result = await orchestrator.optimize_bids(
        campaign_id=campaign_id,
        performance_data=aggregate,
        current_config={
            "budget": campaign.config.brief.budget.model_dump(),
            "channels": [a.model_dump() for a in campaign.config.channel_allocations],
        },
    )

    return ApiResponse(
        data={"campaign_id": campaign_id, "optimization": result},
        message="최적화 분석이 완료되었습니다",
    )
