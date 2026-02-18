"""Analytics and reporting models."""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class MetricSet(BaseModel):
    """채널 공통 메트릭 세트."""

    impressions: int = 0
    clicks: int = 0
    cost: int = 0
    conversions: int = 0
    revenue: int = 0

    @property
    def ctr(self) -> float:
        return (self.clicks / self.impressions * 100) if self.impressions > 0 else 0.0

    @property
    def cpc(self) -> float:
        return (self.cost / self.clicks) if self.clicks > 0 else 0.0

    @property
    def cpa(self) -> float:
        return (self.cost / self.conversions) if self.conversions > 0 else 0.0

    @property
    def roas(self) -> float:
        return (self.revenue / self.cost * 100) if self.cost > 0 else 0.0

    @property
    def cvr(self) -> float:
        return (self.conversions / self.clicks * 100) if self.clicks > 0 else 0.0


class DailyStats(BaseModel):
    date: date
    channel: str
    campaign_id: str
    metrics: MetricSet


class ChannelPerformance(BaseModel):
    channel: str
    metrics: MetricSet
    vs_target: Optional[dict] = None
    top_keywords: list[dict] = Field(default_factory=list)
    top_creatives: list[dict] = Field(default_factory=list)
    insights: Optional[str] = None


class PerformanceData(BaseModel):
    """성과 데이터 조회 결과."""

    campaign_id: str
    period_start: date
    period_end: date
    total_metrics: MetricSet
    channel_breakdown: list[ChannelPerformance] = Field(default_factory=list)
    daily_breakdown: list[DailyStats] = Field(default_factory=list)


class PerformanceReport(BaseModel):
    """AI가 생성하는 성과 분석 리포트."""

    campaign_id: str
    report_type: str  # "daily" | "weekly" | "monthly" | "custom"
    period_start: date
    period_end: date
    executive_summary: str
    total_metrics: MetricSet
    channel_performance: list[ChannelPerformance] = Field(default_factory=list)
    comparison: Optional[dict] = None  # vs previous period
    recommendations: list[dict] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=datetime.now)


class PerformanceQuery(BaseModel):
    campaign_id: str
    start_date: date
    end_date: date
    channels: list[str] = Field(default_factory=list)
    metrics: list[str] = Field(
        default_factory=lambda: [
            "impressions",
            "clicks",
            "cost",
            "conversions",
            "revenue",
        ]
    )
    granularity: str = "daily"  # "daily" | "weekly" | "monthly"


class AlertConfig(BaseModel):
    """성과 이상 감지 알림 설정."""

    campaign_id: str
    metric: str
    condition: str  # "above" | "below"
    threshold: float
    channel: Optional[str] = None
    is_active: bool = True
