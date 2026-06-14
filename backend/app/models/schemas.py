from typing import Any, Optional

from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    dataset_id: str
    filename: str
    rows: int
    columns: int
    column_names: list[str]


class ColumnSummary(BaseModel):
    name: str
    dtype: str
    non_null: int
    null_count: int
    unique: int
    sample_values: list[Any] = Field(default_factory=list)
    min: Optional[float] = None
    max: Optional[float] = None
    mean: Optional[float] = None
    std: Optional[float] = None


class DatasetSummary(BaseModel):
    dataset_id: str
    filename: str
    rows: int
    columns: int
    memory_usage_mb: float
    column_summaries: list[ColumnSummary]
    preview: list[dict[str, Any]]


class ChartSpec(BaseModel):
    id: str
    title: str
    chart_type: str
    columns: list[str]
    figure: dict[str, Any]


class ChartsResponse(BaseModel):
    dataset_id: str
    charts: list[ChartSpec]


class InsightsRequest(BaseModel):
    question: Optional[str] = None


class InsightsResponse(BaseModel):
    dataset_id: str
    insights: str
    question: Optional[str] = None


class ErrorResponse(BaseModel):
    detail: str
