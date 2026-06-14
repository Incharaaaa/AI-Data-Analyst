import { useCallback, useState } from "react";
import { ChartGrid } from "../components/ChartGrid";
import { DatasetSummaryView } from "../components/DatasetSummary";
import { FileUpload } from "../components/FileUpload";
import { InsightsPanel } from "../components/InsightsPanel";
import {
  fetchCharts,
  fetchInsights,
  fetchSummary,
  uploadFile,
} from "../services/api";
import type {
  AnalysisTab,
  ChartsResponse,
  DatasetSummary,
  UploadResponse,
} from "../types";

export function Dashboard() {
  const [upload, setUpload] = useState<UploadResponse | null>(null);
  const [summary, setSummary] = useState<DatasetSummary | null>(null);
  const [charts, setCharts] = useState<ChartsResponse | null>(null);
  const [insights, setInsights] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<AnalysisTab>("summary");
  const [loading, setLoading] = useState(false);
  const [insightsLoading, setInsightsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleUpload = useCallback(async (file: File) => {
    setLoading(true);
    setError(null);
    setUpload(null);
    setSummary(null);
    setCharts(null);
    setInsights(null);

    try {
      const result = await uploadFile(file);
      setUpload(result);

      const [summaryData, chartsData] = await Promise.all([
        fetchSummary(result.dataset_id),
        fetchCharts(result.dataset_id),
      ]);
      setSummary(summaryData);
      setCharts(chartsData);
      setActiveTab("summary");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Upload failed");
    } finally {
      setLoading(false);
    }
  }, []);

  const handleInsights = useCallback(
    async (question?: string) => {
      if (!upload) return;
      setInsightsLoading(true);
      setError(null);
      try {
        const result = await fetchInsights(upload.dataset_id, question);
        setInsights(result.insights);
        setActiveTab("insights");
      } catch (e) {
        setError(e instanceof Error ? e.message : "Insight generation failed");
      } finally {
        setInsightsLoading(false);
      }
    },
    [upload]
  );

  const tabs: { id: AnalysisTab; label: string }[] = [
    { id: "summary", label: "Summary" },
    { id: "charts", label: "Charts" },
    { id: "insights", label: "AI Insights" },
  ];

  return (
    <div style={{ maxWidth: 1200, margin: "0 auto", padding: "2rem 1.5rem" }}>
      <header style={{ marginBottom: "2rem" }}>
        <h1 style={{ fontSize: "1.75rem" }}>AI Data Analyst</h1>
        <p style={{ color: "var(--text-muted)", margin: 0 }}>
          Upload CSV/XLSX, explore summaries, auto-generate charts, and get Gemini insights.
        </p>
      </header>

      {!upload && <FileUpload onUpload={handleUpload} loading={loading} />}

      {error && (
        <div className="error-banner" style={{ marginTop: "1rem" }}>
          {error}
        </div>
      )}

      {upload && (
        <>
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              marginBottom: "1.25rem",
            }}
          >
            <div>
              <h2 style={{ fontSize: "1.25rem" }}>{upload.filename}</h2>
              <p style={{ color: "var(--text-muted)", margin: 0, fontSize: "0.9rem" }}>
                {upload.rows.toLocaleString()} rows · {upload.columns} columns
              </p>
            </div>
            <button
              className="btn btn-ghost"
              onClick={() => {
                setUpload(null);
                setSummary(null);
                setCharts(null);
                setInsights(null);
                setError(null);
              }}
            >
              Upload new file
            </button>
          </div>

          <div className="tabs">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                className={`tab ${activeTab === tab.id ? "active" : ""}`}
                onClick={() => setActiveTab(tab.id)}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {activeTab === "summary" && summary && <DatasetSummaryView summary={summary} />}
          {activeTab === "charts" && charts && <ChartGrid charts={charts.charts} />}
          {activeTab === "insights" && (
            <InsightsPanel
              insights={insights}
              loading={insightsLoading}
              onGenerate={handleInsights}
            />
          )}
        </>
      )}
    </div>
  );
}
