"""SQLite database setup and connection management."""

import aiosqlite
import structlog

logger = structlog.get_logger()

DB_PATH = "data/ad_agent.db"

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS campaigns (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'draft',
    brief_json TEXT NOT NULL,
    config_json TEXT NOT NULL,
    strategy_summary TEXT,
    risk_assessment_json TEXT DEFAULT '[]',
    channel_campaign_ids_json TEXT DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS ad_groups (
    id TEXT PRIMARY KEY,
    campaign_id TEXT NOT NULL,
    channel TEXT NOT NULL,
    name TEXT NOT NULL,
    config_json TEXT NOT NULL,
    channel_adgroup_id TEXT,
    status TEXT NOT NULL DEFAULT 'active',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
);

CREATE TABLE IF NOT EXISTS ads (
    id TEXT PRIMARY KEY,
    ad_group_id TEXT NOT NULL,
    channel TEXT NOT NULL,
    headline TEXT NOT NULL,
    description TEXT NOT NULL,
    display_url TEXT,
    landing_url TEXT,
    creative_config_json TEXT,
    channel_ad_id TEXT,
    status TEXT NOT NULL DEFAULT 'active',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (ad_group_id) REFERENCES ad_groups(id)
);

CREATE TABLE IF NOT EXISTS creatives (
    id TEXT PRIMARY KEY,
    campaign_id TEXT NOT NULL,
    channel TEXT NOT NULL,
    config_json TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'draft',
    review_notes TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
);

CREATE TABLE IF NOT EXISTS daily_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id TEXT NOT NULL,
    channel TEXT NOT NULL,
    stat_date TEXT NOT NULL,
    impressions INTEGER DEFAULT 0,
    clicks INTEGER DEFAULT 0,
    cost INTEGER DEFAULT 0,
    conversions INTEGER DEFAULT 0,
    revenue INTEGER DEFAULT 0,
    raw_data_json TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id),
    UNIQUE(campaign_id, channel, stat_date)
);

CREATE TABLE IF NOT EXISTS channel_accounts (
    id TEXT PRIMARY KEY,
    channel TEXT NOT NULL UNIQUE,
    credentials_json TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1,
    last_verified_at TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS agent_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id TEXT,
    agent_name TEXT NOT NULL,
    action TEXT NOT NULL,
    input_json TEXT,
    output_json TEXT,
    tokens_used INTEGER DEFAULT 0,
    duration_ms INTEGER DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS optimization_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id TEXT NOT NULL,
    channel TEXT,
    optimization_type TEXT NOT NULL,
    before_json TEXT,
    after_json TEXT,
    reason TEXT,
    applied INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
);

CREATE TABLE IF NOT EXISTS visual_assets (
    id TEXT PRIMARY KEY,
    campaign_id TEXT NOT NULL,
    creative_id TEXT,
    channel TEXT NOT NULL,
    format TEXT NOT NULL,
    asset_type TEXT NOT NULL DEFAULT 'image',
    status TEXT NOT NULL DEFAULT 'pending',
    raw_image_path TEXT,
    composite_path TEXT,
    visual_brief_json TEXT,
    text_overlay_json TEXT,
    review_feedback TEXT,
    canva_edit_url TEXT,
    generation_cost_usd REAL DEFAULT 0.0,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
);

CREATE INDEX IF NOT EXISTS idx_daily_stats_campaign ON daily_stats(campaign_id, stat_date);
CREATE INDEX IF NOT EXISTS idx_ads_adgroup ON ads(ad_group_id);
CREATE INDEX IF NOT EXISTS idx_adgroups_campaign ON ad_groups(campaign_id);
CREATE INDEX IF NOT EXISTS idx_agent_logs_campaign ON agent_logs(campaign_id);
CREATE INDEX IF NOT EXISTS idx_visual_assets_campaign ON visual_assets(campaign_id);
CREATE INDEX IF NOT EXISTS idx_visual_assets_status ON visual_assets(status);
"""


class Database:
    def __init__(self, db_path: str = DB_PATH) -> None:
        self.db_path = db_path
        self._db: aiosqlite.Connection | None = None

    async def connect(self) -> None:
        self._db = await aiosqlite.connect(self.db_path)
        self._db.row_factory = aiosqlite.Row
        await self._db.executescript(SCHEMA_SQL)
        await self._db.commit()
        logger.info("database_connected", path=self.db_path)

    async def close(self) -> None:
        if self._db:
            await self._db.close()
            logger.info("database_closed")

    @property
    def db(self) -> aiosqlite.Connection:
        if self._db is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self._db

    async def execute(self, sql: str, params: tuple = ()) -> aiosqlite.Cursor:
        cursor = await self.db.execute(sql, params)
        await self.db.commit()
        return cursor

    async def fetch_one(self, sql: str, params: tuple = ()) -> dict | None:
        cursor = await self.db.execute(sql, params)
        row = await cursor.fetchone()
        if row is None:
            return None
        return dict(row)

    async def fetch_all(self, sql: str, params: tuple = ()) -> list[dict]:
        cursor = await self.db.execute(sql, params)
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]
