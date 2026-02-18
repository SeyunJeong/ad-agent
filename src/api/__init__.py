from src.api.campaigns import router as campaigns_router
from src.api.channels import router as channels_router
from src.api.creative import router as creative_router
from src.api.analytics import router as analytics_router
from src.api.strategy import router as strategy_router
from src.api.visuals import router as visuals_router

__all__ = [
    "campaigns_router",
    "channels_router",
    "creative_router",
    "analytics_router",
    "strategy_router",
    "visuals_router",
]
