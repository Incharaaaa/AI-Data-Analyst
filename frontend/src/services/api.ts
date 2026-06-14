import type {
  ChartsResponse,
  DatasetSummary,
  InsightsResponse,
  UploadResponse,
} from "../types";

const API_BASE = "https://ai-data-analyst-backend-nhrt.onrender.com";

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || "Request failed");
  }
  return res.json();
}

export async function uploadFile(file: File): Promise<UploadResponse> {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${API_BASE}/api/upload`, { method: "POST", body: form });
  return handleResponse<UploadResponse>(res);
}

export async function fetchSummary(datasetId: string): Promise<DatasetSummary> {
  const res = await fetch(`${API_BASE}/api/datasets/${datasetId}/summary`);
  return handleResponse<DatasetSummary>(res);
}

export async function fetchCharts(datasetId: string): Promise<ChartsResponse> {
  const res = await fetch(`${API_BASE}/api/datasets/${datasetId}/charts`);
  return handleResponse<ChartsResponse>(res);
}

export async function fetchInsights(
  datasetId: string,
  question?: string
): Promise<InsightsResponse> {
  const res = await fetch(`${API_BASE}/api/datasets/${datasetId}/insights`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question: question || null }),
  });
  return handleResponse<InsightsResponse>(res);
}
