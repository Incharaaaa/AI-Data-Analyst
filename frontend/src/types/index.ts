export interface UploadResponse {
  dataset_id: string;
  filename: string;
  rows: number;
  columns: number;
  column_names: string[];
}

export interface ColumnSummary {
  name: string;
  dtype: string;
  non_null: number;
  null_count: number;
  unique: number;
  sample_values: unknown[];
  min?: number;
  max?: number;
  mean?: number;
  std?: number;
}

export interface DatasetSummary {
  dataset_id: string;
  filename: string;
  rows: number;
  columns: number;
  memory_usage_mb: number;
  column_summaries: ColumnSummary[];
  preview: Record<string, unknown>[];
}

export interface ChartSpec {
  id: string;
  title: string;
  chart_type: string;
  columns: string[];
  figure: Record<string, unknown>;
}

export interface ChartsResponse {
  dataset_id: string;
  charts: ChartSpec[];
}

export interface InsightsResponse {
  dataset_id: string;
  insights: string;
  question?: string;
}

export type AnalysisTab = "summary" | "charts" | "insights";
