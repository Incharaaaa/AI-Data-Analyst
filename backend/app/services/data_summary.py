import pandas as pd

from app.models.schemas import ColumnSummary, DatasetSummary
from app.services.data_loader import DatasetStore, dataframe_preview, load_dataframe


def _safe_numeric_stats(series: pd.Series) -> dict:
    if not pd.api.types.is_numeric_dtype(series):
        return {}
    clean = series.dropna()
    if clean.empty:
        return {}
    return {
        "min": float(clean.min()),
        "max": float(clean.max()),
        "mean": float(clean.mean()),
        "std": float(clean.std()) if len(clean) > 1 else 0.0,
    }


def summarize_column(df: pd.DataFrame, col: str) -> ColumnSummary:
    series = df[col]
    stats = _safe_numeric_stats(series)
    samples = series.dropna().head(5).tolist()
    samples = [s.isoformat() if hasattr(s, "isoformat") else s for s in samples]

    return ColumnSummary(
        name=col,
        dtype=str(series.dtype),
        non_null=int(series.notna().sum()),
        null_count=int(series.isna().sum()),
        unique=int(series.nunique(dropna=True)),
        sample_values=samples,
        **stats,
    )


def build_dataset_summary(dataset_id: str) -> DatasetSummary:
    meta = DatasetStore.get(dataset_id)
    df = load_dataframe(dataset_id)

    memory_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)
    column_summaries = [summarize_column(df, col) for col in df.columns]

    return DatasetSummary(
        dataset_id=dataset_id,
        filename=meta["filename"],
        rows=len(df),
        columns=len(df.columns),
        memory_usage_mb=round(memory_mb, 3),
        column_summaries=column_summaries,
        preview=dataframe_preview(df),
    )
