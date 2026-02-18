"""Ad Agent — FastAPI application entry point."""

import os
from contextlib import asynccontextmanager
from pathlib import Path

import structlog
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.agents.orchestrator import AgentOrchestrator
from src.api import (
    analytics_router,
    campaigns_router,
    channels_router,
    creative_router,
    strategy_router,
)
from src.channels.registry import ChannelRegistry
from src.config.settings import get_settings
from src.storage.database import Database
from src.storage.repositories import AgentLogRepository

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup/shutdown."""
    settings = get_settings()

    # Ensure data directory exists
    Path("data").mkdir(exist_ok=True)

    # Database
    db = Database()
    await db.connect()
    app.state.db = db

    # Channel Registry
    app.state.channel_registry = ChannelRegistry(settings)

    # Agent Orchestrator
    log_repo = AgentLogRepository(db)
    app.state.orchestrator = AgentOrchestrator(settings, log_repo)

    logger.info(
        "ad_agent_started",
        host=settings.host,
        port=settings.port,
        debug=settings.debug,
    )

    yield

    # Shutdown
    await db.close()
    logger.info("ad_agent_stopped")


app = FastAPI(
    title="Ad Agent API",
    description="AI-powered performance marketing platform for Korean market",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(campaigns_router, prefix="/v1")
app.include_router(strategy_router, prefix="/v1")
app.include_router(creative_router, prefix="/v1")
app.include_router(analytics_router, prefix="/v1")
app.include_router(channels_router, prefix="/v1")


@app.get("/")
async def root():
    return {
        "name": "Ad Agent",
        "version": "0.1.0",
        "description": "AI 퍼포먼스 마케팅 플랫폼",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    return {"status": "ok"}


def run():
    settings = get_settings()
    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )


if __name__ == "__main__":
    run()
