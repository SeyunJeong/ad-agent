"""Visual asset generation and management endpoints."""

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Request

from src.models.visual import (
    VisualAsset,
    VisualGenerationRequest,
    VisualGenerationResponse,
    VisualReviewRequest,
    VisualReviewResponse,
    VisualStatus,
)
from src.services.visual_director import VisualDirectorService

router = APIRouter(prefix="/visuals", tags=["visuals"])


def get_visual_director(request: Request) -> VisualDirectorService:
    director = getattr(request.app.state, "visual_director", None)
    if director is None:
        raise HTTPException(
            status_code=503,
            detail="Visual generation not available. Configure FAL_API_KEY and CREATOMATE_API_KEY.",
        )
    return director


VisualDirector = Annotated[VisualDirectorService, Depends(get_visual_director)]


@router.post("/generate", response_model=VisualGenerationResponse)
async def generate_visuals(
    request: VisualGenerationRequest,
    director: VisualDirector,
):
    """Generate visual assets for a campaign.

    Creates AI images via Flux 2.0 Pro, then overlays Korean text via Creatomate.
    All assets start in DRAFT status awaiting review.
    """
    try:
        return await director.generate_visuals(request)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.get("/campaigns/{campaign_id}", response_model=list[VisualAsset])
async def list_campaign_visuals(
    campaign_id: str,
    director: VisualDirector,
    status: Optional[str] = None,
):
    """List all visual assets for a campaign, optionally filtered by status."""
    return await director.get_campaign_assets(campaign_id, status)


@router.get("/{asset_id}", response_model=VisualAsset)
async def get_visual_asset(
    asset_id: str,
    director: VisualDirector,
):
    """Get a single visual asset by ID."""
    assets = await director._repo.get(asset_id)
    if not assets:
        raise HTTPException(status_code=404, detail="Asset not found")
    return assets


@router.post("/{asset_id}/review", response_model=VisualReviewResponse)
async def review_visual(
    asset_id: str,
    review: VisualReviewRequest,
    director: VisualDirector,
):
    """Review a visual asset: approve, reject, or send to Canva for editing.

    Actions:
    - approve: Mark as APPROVED (ready for ad deployment)
    - reject: Mark as REJECTED with feedback (can regenerate)
    - edit: Open in Canva for human editing
    """
    try:
        asset = await director.review_asset(asset_id, review.action, review.feedback)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return VisualReviewResponse(
        asset_id=asset.id,
        new_status=asset.status,
        canva_edit_url=asset.canva_edit_url,
        message=f"Asset {asset_id} {review.action}d successfully",
    )


@router.post("/{asset_id}/regenerate", response_model=VisualAsset)
async def regenerate_visual(
    asset_id: str,
    request: VisualGenerationRequest,
    director: VisualDirector,
):
    """Regenerate a rejected visual asset with updated parameters."""
    try:
        return await director.regenerate_asset(asset_id, request)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/batch/approve")
async def batch_approve(
    asset_ids: list[str],
    director: VisualDirector,
):
    """Approve multiple visual assets at once."""
    results = []
    for aid in asset_ids:
        try:
            asset = await director.review_asset(aid, "approve")
            results.append({"asset_id": aid, "status": "approved"})
        except ValueError:
            results.append({"asset_id": aid, "status": "not_found"})
    return {"results": results}


@router.delete("/{asset_id}")
async def delete_visual(
    asset_id: str,
    director: VisualDirector,
):
    """Delete a visual asset."""
    await director._repo.delete(asset_id)
    return {"message": f"Asset {asset_id} deleted"}
