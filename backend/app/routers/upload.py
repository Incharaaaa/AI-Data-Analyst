from fastapi import APIRouter, File, HTTPException, UploadFile

from app.config import settings
from app.models.schemas import UploadResponse
from app.services.data_loader import DatasetStore, load_dataframe, save_upload
from app.utils.file_validator import validate_extension, validate_file_size

router = APIRouter(prefix="/api", tags=["upload"])


@router.post("/upload", response_model=UploadResponse)
async def upload_dataset(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    try:
        validate_extension(file.filename)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    content = await file.read()
    try:
        validate_file_size(len(content), settings.max_upload_mb)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    try:
        dataset_id, _ = save_upload(content, file.filename)
        df = load_dataframe(dataset_id)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Failed to parse file: {e}") from e

    return UploadResponse(
        dataset_id=dataset_id,
        filename=file.filename,
        rows=len(df),
        columns=len(df.columns),
        column_names=df.columns.tolist(),
    )
