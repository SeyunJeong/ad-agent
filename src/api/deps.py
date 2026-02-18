"""FastAPI dependencies — shared across all routers."""

from typing import Annotated

from fastapi import Depends, Request

from src.agents.orchestrator import AgentOrchestrator
from src.channels.registry import ChannelRegistry
from src.config.settings import Settings, get_settings
from src.storage.database import Database
from src.storage.repositories import AgentLogRepository, CampaignRepository, StatsRepository


def get_db(request: Request) -> Database:
    return request.app.state.db


def get_campaign_repo(db: Database = Depends(get_db)) -> CampaignRepository:
    return CampaignRepository(db)


def get_stats_repo(db: Database = Depends(get_db)) -> StatsRepository:
    return StatsRepository(db)


def get_agent_log_repo(db: Database = Depends(get_db)) -> AgentLogRepository:
    return AgentLogRepository(db)


def get_channel_registry(request: Request) -> ChannelRegistry:
    return request.app.state.channel_registry


def get_orchestrator(request: Request) -> AgentOrchestrator:
    return request.app.state.orchestrator


# Type aliases for cleaner route signatures
Db = Annotated[Database, Depends(get_db)]
CampaignRepo = Annotated[CampaignRepository, Depends(get_campaign_repo)]
StatsRepo = Annotated[StatsRepository, Depends(get_stats_repo)]
Channels = Annotated[ChannelRegistry, Depends(get_channel_registry)]
Orchestrator = Annotated[AgentOrchestrator, Depends(get_orchestrator)]
