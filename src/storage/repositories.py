"""Database repositories — CRUD operations."""

import json
from datetime import datetime
from typing import Optional

from src.models.campaign import Campaign, CampaignBrief, CampaignConfig, CampaignFilters, CampaignStatus
from src.models.visual import AssetType, ChannelFormat, VisualAsset, VisualStatus
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


class VisualAssetRepository:
    def __init__(self, db: Database) -> None:
        self._db = db

    async def create(self, asset: VisualAsset) -> VisualAsset:
        await self._db.execute(
            """INSERT INTO visual_assets
               (id, campaign_id, creative_id, channel, format, asset_type, status,
                raw_image_path, composite_path, visual_brief_json, text_overlay_json,
                review_feedback, canva_edit_url, generation_cost_usd, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                asset.id,
                asset.campaign_id,
                asset.creative_id,
                asset.channel,
                asset.format.value,
                asset.asset_type.value,
                asset.status.value,
                asset.raw_image_path,
                asset.composite_path,
                json.dumps(asset.visual_brief) if asset.visual_brief else None,
                json.dumps(asset.text_overlay) if asset.text_overlay else None,
                asset.review_feedback,
                asset.canva_edit_url,
                asset.generation_cost_usd,
                asset.created_at.isoformat(),
                asset.updated_at.isoformat(),
            ),
        )
        return asset

    async def get(self, asset_id: str) -> Optional[VisualAsset]:
        row = await self._db.fetch_one(
            "SELECT * FROM visual_assets WHERE id = ?", (asset_id,)
        )
        if not row:
            return None
        return self._row_to_asset(row)

    async def list_by_campaign(
        self, campaign_id: str, status: Optional[str] = None
    ) -> list[VisualAsset]:
        sql = "SELECT * FROM visual_assets WHERE campaign_id = ?"
        params: list = [campaign_id]
        if status:
            sql += " AND status = ?"
            params.append(status)
        sql += " ORDER BY created_at DESC"
        rows = await self._db.fetch_all(sql, tuple(params))
        return [self._row_to_asset(r) for r in rows]

    async def update_status(
        self, asset_id: str, status: VisualStatus, **kwargs
    ) -> Optional[VisualAsset]:
        sets = ["status = ?", "updated_at = ?"]
        params: list = [status.value, datetime.now().isoformat()]
        for key, val in kwargs.items():
            if key in (
                "raw_image_path", "composite_path", "review_feedback",
                "canva_edit_url", "generation_cost_usd",
            ):
                sets.append(f"{key} = ?")
                params.append(val)
        params.append(asset_id)
        await self._db.execute(
            f"UPDATE visual_assets SET {', '.join(sets)} WHERE id = ?",
            tuple(params),
        )
        return await self.get(asset_id)

    async def delete(self, asset_id: str) -> None:
        await self._db.execute(
            "DELETE FROM visual_assets WHERE id = ?", (asset_id,)
        )

    def _row_to_asset(self, row: dict) -> VisualAsset:
        return VisualAsset(
            id=row["id"],
            campaign_id=row["campaign_id"],
            creative_id=row.get("creative_id"),
            channel=row["channel"],
            format=ChannelFormat(row["format"]),
            asset_type=AssetType(row["asset_type"]),
            status=VisualStatus(row["status"]),
            raw_image_path=row.get("raw_image_path"),
            composite_path=row.get("composite_path"),
            visual_brief=json.loads(row["visual_brief_json"]) if row.get("visual_brief_json") else None,
            text_overlay=json.loads(row["text_overlay_json"]) if row.get("text_overlay_json") else None,
            review_feedback=row.get("review_feedback"),
            canva_edit_url=row.get("canva_edit_url"),
            generation_cost_usd=row.get("generation_cost_usd", 0.0),
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )


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
