from fastapi import APIRouter, HTTPException

from app.models.schemas import InsightsRequest, InsightsResponse
from app.services.data_loader import DatasetStore
from app.services.gemini_insights import generate_insights

router = APIRouter(prefix="/api/datasets", tags=["insights"])


@router.post("/{dataset_id}/insights", response_model=InsightsResponse)
async def get_insights(dataset_id: str, body: InsightsRequest | None = None):
    if not DatasetStore.exists(dataset_id):
        raise HTTPException(status_code=404, detail=f"Dataset '{dataset_id}' not found")

    question = body.question if body else None

    try:
        insights = generate_insights(dataset_id, question)
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Insight generation failed: {e}") from e

    return InsightsResponse(
        dataset_id=dataset_id,
        insights=insights,
        question=question,
    )
