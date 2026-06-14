import google.generativeai as genai

from app.config import settings
from app.services.data_loader import DatasetStore, load_dataframe
from app.services.data_summary import build_dataset_summary


def _build_context(dataset_id: str) -> str:
    summary = build_dataset_summary(dataset_id)
    df = load_dataframe(dataset_id)

    lines = [
        f"Dataset: {summary.filename}",
        f"Rows: {summary.rows}, Columns: {summary.columns}",
        f"Memory: {summary.memory_usage_mb} MB",
        "",
        "Column overview:",
    ]

    for col in summary.column_summaries:
        parts = [
            f"  - {col.name} ({col.dtype}): {col.non_null} non-null, {col.unique} unique"
        ]
        if col.mean is not None:
            parts.append(
                f"    stats: min={col.min}, max={col.max}, mean={col.mean:.2f}, std={col.std:.2f}"
            )
        if col.sample_values:
            parts.append(f"    samples: {col.sample_values[:3]}")
        lines.extend(parts)

    desc = df.describe(include="all").to_string()
    lines.extend(["", "Pandas describe():", desc])

    return "\n".join(lines)


def generate_insights(dataset_id: str, question: str | None = None) -> str:
    if not settings.gemini_api_key:
        raise ValueError(
            "GEMINI_API_KEY is not configured. Add it to backend/.env to enable AI insights."
        )

    meta = DatasetStore.get(dataset_id)
    context = _build_context(dataset_id)

    genai.configure(api_key=settings.gemini_api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")

    user_prompt = question or (
        "Analyze this dataset and provide actionable insights. Include: "
        "key patterns, anomalies, data quality issues, and 3-5 recommended "
        "follow-up analyses. Be concise and use bullet points."
    )

    prompt = f"""You are an expert data analyst assistant.

Dataset context:
{context}

User request:
{user_prompt}
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"""
    AI insights are temporarily unavailable.

    Reason:
    {str(e)}

    Suggested analysis:
    • Check missing values
    • Identify outliers
    • Compare distributions
    • Analyze correlations
    • Review data quality
    """
