import json
import uuid

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from app.models.schemas import ChartSpec, ChartsResponse
from app.services.data_loader import load_dataframe

MAX_CHARTS = 8
MAX_CATEGORIES = 20


def _fig_to_dict(fig: go.Figure) -> dict:
    return json.loads(fig.to_json())


def _numeric_columns(df: pd.DataFrame) -> list[str]:
    return df.select_dtypes(include="number").columns.tolist()


def _categorical_columns(df: pd.DataFrame) -> list[str]:
    return df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()


def _datetime_columns(df: pd.DataFrame) -> list[str]:
    return df.select_dtypes(include=["datetime", "datetimetz"]).columns.tolist()


def generate_charts(dataset_id: str) -> ChartsResponse:
    df = load_dataframe(dataset_id)
    charts: list[ChartSpec] = []

    numeric = _numeric_columns(df)
    categorical = _categorical_columns(df)
    datetime_cols = _datetime_columns(df)

    # Histogram for each numeric column (up to 3)
    for col in numeric[:3]:
        fig = px.histogram(df, x=col, title=f"Distribution of {col}", nbins=30)
        fig.update_layout(margin=dict(t=50, b=40, l=40, r=20))
        charts.append(
            ChartSpec(
                id=str(uuid.uuid4()),
                title=f"Distribution of {col}",
                chart_type="histogram",
                columns=[col],
                figure=_fig_to_dict(fig),
            )
        )

    # Bar chart for categorical value counts (up to 2)
    for col in categorical[:2]:
        counts = df[col].value_counts().head(MAX_CATEGORIES).reset_index()
        counts.columns = [col, "count"]
        fig = px.bar(counts, x=col, y="count", title=f"Top values in {col}")
        fig.update_layout(margin=dict(t=50, b=80, l=40, r=20))
        charts.append(
            ChartSpec(
                id=str(uuid.uuid4()),
                title=f"Top values in {col}",
                chart_type="bar",
                columns=[col],
                figure=_fig_to_dict(fig),
            )
        )

    # Scatter for first two numeric columns
    if len(numeric) >= 2:
        x_col, y_col = numeric[0], numeric[1]
        fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            title=f"{y_col} vs {x_col}",
            opacity=0.6,
        )
        fig.update_layout(margin=dict(t=50, b=40, l=40, r=20))
        charts.append(
            ChartSpec(
                id=str(uuid.uuid4()),
                title=f"{y_col} vs {x_col}",
                chart_type="scatter",
                columns=[x_col, y_col],
                figure=_fig_to_dict(fig),
            )
        )

    # Correlation heatmap when 2+ numeric columns
    if len(numeric) >= 2:
        corr = df[numeric].corr()
        fig = px.imshow(
            corr,
            text_auto=".2f",
            title="Correlation Heatmap",
            color_continuous_scale="RdBu_r",
            zmin=-1,
            zmax=1,
        )
        fig.update_layout(margin=dict(t=50, b=40, l=40, r=20))
        charts.append(
            ChartSpec(
                id=str(uuid.uuid4()),
                title="Correlation Heatmap",
                chart_type="heatmap",
                columns=numeric,
                figure=_fig_to_dict(fig),
            )
        )

    # Time series if datetime + numeric
    if datetime_cols and numeric:
        dt_col = datetime_cols[0]
        num_col = numeric[0]
        ts_df = df[[dt_col, num_col]].dropna().sort_values(dt_col)
        if not ts_df.empty:
            fig = px.line(
                ts_df,
                x=dt_col,
                y=num_col,
                title=f"{num_col} over time",
            )
            fig.update_layout(margin=dict(t=50, b=40, l=40, r=20))
            charts.append(
                ChartSpec(
                    id=str(uuid.uuid4()),
                    title=f"{num_col} over time",
                    chart_type="line",
                    columns=[dt_col, num_col],
                    figure=_fig_to_dict(fig),
                )
            )

    # Box plot for numeric grouped by first categorical
    if numeric and categorical:
        num_col = numeric[0]
        cat_col = categorical[0]
        top_cats = df[cat_col].value_counts().head(10).index.tolist()
        filtered = df[df[cat_col].isin(top_cats)]
        fig = px.box(
            filtered,
            x=cat_col,
            y=num_col,
            title=f"{num_col} by {cat_col}",
        )
        fig.update_layout(margin=dict(t=50, b=80, l=40, r=20))
        charts.append(
            ChartSpec(
                id=str(uuid.uuid4()),
                title=f"{num_col} by {cat_col}",
                chart_type="box",
                columns=[cat_col, num_col],
                figure=_fig_to_dict(fig),
            )
        )

    return ChartsResponse(dataset_id=dataset_id, charts=charts[:MAX_CHARTS])
