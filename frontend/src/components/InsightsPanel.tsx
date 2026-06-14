import { useState } from "react";

interface InsightsPanelProps {
  insights: string | null;
  loading: boolean;
  onGenerate: (question?: string) => void;
}

export function InsightsPanel({ insights, loading, onGenerate }: InsightsPanelProps) {
  const [question, setQuestion] = useState("");

  return (
    <div>
      <p style={{ color: "var(--text-muted)", marginBottom: "1rem" }}>
        Get AI-powered analysis of your dataset using Google Gemini.
      </p>

      <div style={{ display: "flex", gap: "0.75rem", marginBottom: "1.25rem" }}>
        <input
          type="text"
          placeholder="Optional: ask a specific question about your data..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          style={{
            flex: 1,
            padding: "0.65rem 0.9rem",
            borderRadius: "8px",
            border: "1px solid var(--border)",
            background: "var(--surface-2)",
            color: "var(--text)",
            fontSize: "0.9rem",
          }}
        />
        <button
          className="btn btn-primary"
          disabled={loading}
          onClick={() => onGenerate(question.trim() || undefined)}
        >
          {loading ? "Generating..." : insights ? "Regenerate" : "Generate Insights"}
        </button>
      </div>

      {loading && <p className="loading">Analyzing dataset with Gemini...</p>}

      {insights && !loading && (
        <div className="card insights-text">{insights}</div>
      )}
    </div>
  );
}
