"""Application settings via Pydantic Settings."""

from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    log_level: str = "INFO"

    # Database
    database_url: str = "sqlite+aiosqlite:///data/ad_agent.db"

    # AI
    anthropic_api_key: str = ""
    ai_model: str = "claude-sonnet-4-5-20250929"

    # Naver Search Ads
    naver_api_key: Optional[str] = None
    naver_secret_key: Optional[str] = None
    naver_customer_id: Optional[str] = None

    # Kakao Moment
    kakao_app_key: Optional[str] = None
    kakao_access_token: Optional[str] = None

    # Meta (Facebook/Instagram)
    meta_app_id: Optional[str] = None
    meta_app_secret: Optional[str] = None
    meta_access_token: Optional[str] = None
    meta_ad_account_id: Optional[str] = None

    # Google Ads
    google_developer_token: Optional[str] = None
    google_client_id: Optional[str] = None
    google_client_secret: Optional[str] = None
    google_refresh_token: Optional[str] = None
    google_customer_id: Optional[str] = None

    # Visual Generation APIs
    fal_api_key: Optional[str] = None
    creatomate_api_key: Optional[str] = None
    runway_api_key: Optional[str] = None
    heygen_api_key: Optional[str] = None
    canva_api_key: Optional[str] = None

    # API Auth
    api_secret_key: str = "change-this-to-random-secret"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    @property
    def visual_generation_ready(self) -> bool:
        """At least image gen + compositor must be configured."""
        return bool(self.fal_api_key and self.creatomate_api_key)

    @property
    def naver_configured(self) -> bool:
        return bool(self.naver_api_key and self.naver_secret_key and self.naver_customer_id)

    @property
    def kakao_configured(self) -> bool:
        return bool(self.kakao_app_key and self.kakao_access_token)

    @property
    def meta_configured(self) -> bool:
        return bool(self.meta_access_token and self.meta_ad_account_id)

    @property
    def google_configured(self) -> bool:
        return bool(self.google_developer_token and self.google_refresh_token)


@lru_cache
def get_settings() -> Settings:
    return Settings()
