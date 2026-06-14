import os
import json

STORE_FILE = "dataset_store.json"
import uuid
from pathlib import Path

import pandas as pd

from app.config import settings


class DatasetStore:
    """In-memory registry mapping dataset IDs to file paths and metadata."""

    _registry = {}

    @classmethod
    def _save(cls):
        with open(STORE_FILE, "w") as f:
            json.dump({k: {"filename": v["filename"], "path": str(v["path"])} for k, v in cls._registry.items()}, f)


    @classmethod
    def _load(cls):
        if os.path.exists(STORE_FILE):
            with open(STORE_FILE, "r") as f:
                data = json.load(f)
                cls._registry = {
                    k: {"filename": v["filename"], "path": v["path"]}
                    for k, v in data.items()
            }

    @classmethod
    def register(cls, file_path: Path, filename: str, dataset_id: str) -> str:
        cls._registry[dataset_id] = {
            "path": file_path,
            "filename": filename,
        }
        cls._save()
        return dataset_id

    @classmethod
    def get(cls, dataset_id: str) -> dict:
        if dataset_id not in cls._registry:
            raise KeyError(f"Dataset '{dataset_id}' not found")
        return cls._registry[dataset_id]

    @classmethod
    def exists(cls, dataset_id: str) -> bool:
        return dataset_id in cls._registry


def load_dataframe(dataset_id: str) -> pd.DataFrame:
    meta = DatasetStore.get(dataset_id)
    path: Path = meta["path"]
    ext = path.suffix.lower()

    if ext == ".csv":
        return pd.read_csv(path)
    if ext in {".xlsx", ".xls"}:
        return pd.read_excel(path)

    raise ValueError(f"Unsupported file extension: {ext}")


def save_upload(file_content: bytes, filename: str) -> tuple[str, Path]:
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)

    dataset_id = str(uuid.uuid4())
    ext = Path(filename).suffix.lower()
    file_path = upload_dir / f"{dataset_id}{ext}"

    file_path.write_bytes(file_content)
    DatasetStore.register(file_path, filename, dataset_id)

    return dataset_id, file_path


def dataframe_preview(df: pd.DataFrame, n: int = 10) -> list[dict]:
    preview = df.head(n).copy()
    preview = preview.where(preview.notna(), None)
    return json.loads(preview.to_json(orient="records", date_format="iso"))
DatasetStore._load()
