"""Database repositories — CRUD operations."""

import json
from datetime import datetime
from typing import Optional

from src.models.campaign import Campaign, CampaignBrief, CampaignConfig, CampaignFilters, CampaignStatus
from src.storage.database import Database


class CampaignRepository:
    def __init__(self, db: Database) -> None:
        self._db = db

    async def create(self, campaign: Campaign) -> Campaign:
        await self._db.execute(
            """INSERT INTO campaigns
               (id, name, status, brief_json, config_json, strategy_summary,
                risk_assessment_json, channel_campaign_ids_json, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                campaign.id,
                campaign.config.name,
                campaign.status.value,
                campaign.config.brief.model_dump_json(),
                campaign.config.model_dump_json(),
                campaign.strategy_summary,
                json.dumps(campaign.risk_assessment),
                json.dumps(campaign.channel_campaign_ids),
                campaign.created_at.isoformat(),
                campaign.updated_at.isoformat(),
            ),
        )
        return campaign

    async def get(self, campaign_id: str) -> Optional[Campaign]:
        row = await self._db.fetch_one(
            "SELECT * FROM campaigns WHERE id = ?", (campaign_id,)
        )
        if not row:
            return None
        return self._row_to_campaign(row)

    async def list(
        self, filters: Optional[CampaignFilters] = None
    ) -> list[Campaign]:
        sql = "SELECT * FROM campaigns WHERE 1=1"
        params: list = []
        if filters:
            if filters.status:
                sql += " AND status = ?"
                params.append(filters.status.value)
            if filters.channel:
                sql += " AND config_json LIKE ?"
                params.append(f"%{filters.channel}%")
        sql += " ORDER BY created_at DESC"

        rows = await self._db.fetch_all(sql, tuple(params))
        return [self._row_to_campaign(r) for r in rows]

    async def update(self, campaign: Campaign) -> Campaign:
        campaign.updated_at = datetime.now()
        await self._db.execute(
            """UPDATE campaigns
               SET name=?, status=?, config_json=?, strategy_summary=?,
                   risk_assessment_json=?, channel_campaign_ids_json=?, updated_at=?
               WHERE id=?""",
            (
                campaign.config.name,
                campaign.status.value,
                campaign.config.model_dump_json(),
                campaign.strategy_summary,
                json.dumps(campaign.risk_assessment),
                json.dumps(campaign.channel_campaign_ids),
                campaign.updated_at.isoformat(),
                campaign.id,
            ),
        )
        return campaign

    async def delete(self, campaign_id: str) -> None:
        await self._db.execute(
            "UPDATE campaigns SET status = ? WHERE id = ?",
            (CampaignStatus.ARCHIVED.value, campaign_id),
        )

    def _row_to_campaign(self, row: dict) -> Campaign:
        config = CampaignConfig.model_validate_json(row["config_json"])
        return Campaign(
            id=row["id"],
            config=config,
            status=CampaignStatus(row["status"]),
            strategy_summary=row.get("strategy_summary"),
            risk_assessment=json.loads(row.get("risk_assessment_json", "[]")),
            channel_campaign_ids=json.loads(row.get("channel_campaign_ids_json", "{}")),
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )


class StatsRepository:
    def __init__(self, db: Database) -> None:
        self._db = db

    async def save_daily_stats(
        self,
        campaign_id: str,
        channel: str,
        stat_date: str,
        impressions: int,
        clicks: int,
        cost: int,
        conversions: int,
        revenue: int = 0,
        raw_data: Optional[dict] = None,
    ) -> None:
        await self._db.execute(
            """INSERT OR REPLACE INTO daily_stats
               (campaign_id, channel, stat_date, impressions, clicks, cost,
                conversions, revenue, raw_data_json)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                campaign_id,
                channel,
                stat_date,
                impressions,
                clicks,
                cost,
                conversions,
                revenue,
                json.dumps(raw_data) if raw_data else None,
            ),
        )

    async def get_daily_stats(
        self,
        campaign_id: str,
        start_date: str,
        end_date: str,
        channel: Optional[str] = None,
    ) -> list[dict]:
        sql = """SELECT * FROM daily_stats
                 WHERE campaign_id = ? AND stat_date BETWEEN ? AND ?"""
        params: list = [campaign_id, start_date, end_date]
        if channel:
            sql += " AND channel = ?"
            params.append(channel)
        sql += " ORDER BY stat_date, channel"
        return await self._db.fetch_all(sql, tuple(params))

    async def get_aggregate_stats(
        self,
        campaign_id: str,
        start_date: str,
        end_date: str,
    ) -> dict:
        row = await self._db.fetch_one(
            """SELECT
                 SUM(impressions) as impressions,
                 SUM(clicks) as clicks,
                 SUM(cost) as cost,
                 SUM(conversions) as conversions,
                 SUM(revenue) as revenue
               FROM daily_stats
               WHERE campaign_id = ? AND stat_date BETWEEN ? AND ?""",
            (campaign_id, start_date, end_date),
        )
        return row or {}


class AgentLogRepository:
    def __init__(self, db: Database) -> None:
        self._db = db

    async def log(
        self,
        agent_name: str,
        action: str,
        campaign_id: Optional[str] = None,
        input_data: Optional[dict] = None,
        output_data: Optional[dict] = None,
        tokens_used: int = 0,
        duration_ms: int = 0,
    ) -> None:
        await self._db.execute(
            """INSERT INTO agent_logs
               (campaign_id, agent_name, action, input_json, output_json,
                tokens_used, duration_ms)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                campaign_id,
                agent_name,
                action,
                json.dumps(input_data) if input_data else None,
                json.dumps(output_data) if output_data else None,
                tokens_used,
                duration_ms,
            ),
        )
