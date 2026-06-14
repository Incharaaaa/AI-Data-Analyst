import type { DatasetSummary } from "../types";

interface DatasetSummaryViewProps {
  summary: DatasetSummary;
}

export function DatasetSummaryView({ summary }: DatasetSummaryViewProps) {
  return (
    <div>
      <div className="stat-grid" style={{ marginBottom: "1.5rem" }}>
        <div className="stat-card">
          <div className="label">Rows</div>
          <div className="value">{summary.rows.toLocaleString()}</div>
        </div>
        <div className="stat-card">
          <div className="label">Columns</div>
          <div className="value">{summary.columns}</div>
        </div>
        <div className="stat-card">
          <div className="label">Memory</div>
          <div className="value">{summary.memory_usage_mb} MB</div>
        </div>
        <div className="stat-card">
          <div className="label">File</div>
          <div className="value" style={{ fontSize: "1rem", wordBreak: "break-all" }}>
            {summary.filename}
          </div>
        </div>
      </div>

      <h3>Column Details</h3>
      <div className="preview-table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Column</th>
              <th>Type</th>
              <th>Non-null</th>
              <th>Nulls</th>
              <th>Unique</th>
              <th>Stats</th>
            </tr>
          </thead>
          <tbody>
            {summary.column_summaries.map((col) => (
              <tr key={col.name}>
                <td><strong>{col.name}</strong></td>
                <td><span className="badge">{col.dtype}</span></td>
                <td>{col.non_null}</td>
                <td>{col.null_count}</td>
                <td>{col.unique}</td>
                <td style={{ fontSize: "0.8rem", color: "var(--text-muted)" }}>
                  {col.mean != null
                    ? `μ=${col.mean.toFixed(2)}, σ=${col.std?.toFixed(2)}, [${col.min}–${col.max}]`
                    : col.sample_values.slice(0, 2).map(String).join(", ") || "—"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <h3 style={{ marginTop: "1.5rem" }}>Preview (first 10 rows)</h3>
      <div className="preview-table-wrapper">
        <table>
          <thead>
            <tr>
              {summary.preview.length > 0 &&
                Object.keys(summary.preview[0]).map((key) => (
                  <th key={key}>{key}</th>
                ))}
            </tr>
          </thead>
          <tbody>
            {summary.preview.map((row, i) => (
              <tr key={i}>
                {Object.values(row).map((val, j) => (
                  <td key={j}>{val == null ? "—" : String(val)}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
