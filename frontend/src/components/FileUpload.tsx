import { useCallback, useRef, useState } from "react";

interface FileUploadProps {
  onUpload: (file: File) => void;
  loading: boolean;
}

export function FileUpload({ onUpload, loading }: FileUploadProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragOver, setDragOver] = useState(false);

  const handleFile = useCallback(
    (file: File | undefined) => {
      if (!file) return;
      const ext = file.name.split(".").pop()?.toLowerCase();
      if (!ext || !["csv", "xlsx", "xls"].includes(ext)) {
        alert("Please upload a CSV or XLSX file.");
        return;
      }
      onUpload(file);
    },
    [onUpload]
  );

  return (
    <div
      className="card"
      style={{
        borderStyle: dragOver ? "dashed" : "solid",
        borderColor: dragOver ? "var(--accent)" : undefined,
        textAlign: "center",
        padding: "2.5rem 2rem",
        cursor: loading ? "not-allowed" : "pointer",
      }}
      onDragOver={(e) => {
        e.preventDefault();
        setDragOver(true);
      }}
      onDragLeave={() => setDragOver(false)}
      onDrop={(e) => {
        e.preventDefault();
        setDragOver(false);
        if (!loading) handleFile(e.dataTransfer.files[0]);
      }}
      onClick={() => !loading && inputRef.current?.click()}
    >
      <input
        ref={inputRef}
        type="file"
        accept=".csv,.xlsx,.xls"
        hidden
        onChange={(e) => handleFile(e.target.files?.[0])}
      />
      <div style={{ fontSize: "2.5rem", marginBottom: "0.75rem" }}>📊</div>
      <h2 style={{ marginBottom: "0.5rem" }}>
        {loading ? "Uploading..." : "Upload your dataset"}
      </h2>
      <p style={{ color: "var(--text-muted)", margin: "0 0 1rem" }}>
        Drag & drop or click to select a CSV or XLSX file
      </p>
      <span className="badge">Max 50 MB</span>
    </div>
  );
}
