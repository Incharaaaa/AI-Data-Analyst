import Plot from "react-plotly.js";
import type { ChartSpec } from "../types";

interface ChartGridProps {
  charts: ChartSpec[];
}

export function ChartGrid({ charts }: ChartGridProps) {
  if (charts.length === 0) {
    return (
      <p style={{ color: "var(--text-muted)" }}>
        No charts could be generated for this dataset.
      </p>
    );
  }

  return (
    <div className="chart-grid">
      {charts.map((chart) => (
        <div key={chart.id} className="card">
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "0.5rem" }}>
            <h3 style={{ fontSize: "1rem" }}>{chart.title}</h3>
            <span className="badge">{chart.chart_type}</span>
          </div>
          <Plot
            data={chart.figure.data as Plotly.Data[]}
            layout={{
              ...(chart.figure.layout as Partial<Plotly.Layout>),
              paper_bgcolor: "transparent",
              plot_bgcolor: "transparent",
              font: { color: "#e8edf4", family: "Segoe UI, system-ui, sans-serif" },
              margin: { t: 40, b: 50, l: 50, r: 20 },
            }}
            config={{ responsive: true, displayModeBar: false }}
            style={{ width: "100%", height: "360px" }}
            useResizeHandler
          />
        </div>
      ))}
    </div>
  );
}
