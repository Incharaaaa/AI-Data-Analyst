from fastapi import APIRouter, UploadFile, File
import uuid
import pandas as pd
from app.services.data_loader import DatasetStore

router = APIRouter()

@router.post("/api/upload")
async def upload(file: UploadFile = File(...)):
    dataset_id = str(uuid.uuid4())

    df = pd.read_csv(file.file)

    DatasetStore.save(dataset_id, file.filename, df)

    return {
        "dataset_id": dataset_id,
        "filename": file.filename,
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns),
    }