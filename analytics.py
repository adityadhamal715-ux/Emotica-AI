"""
analytics.py
============
Turns raw detection records from the database into Plotly figures used
on the Analytics page: emotion distribution (pie + bar) and a
detection timeline.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import config
from database import DetectionRecord


def records_to_dataframe(records: list[DetectionRecord]) -> pd.DataFrame:
    if not records:
        return pd.DataFrame(columns=["timestamp", "emotion", "confidence", "song_played"])
    df = pd.DataFrame([r.__dict__ for r in records])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df.sort_values("timestamp")


def _theme_layout(fig: go.Figure, title: str) -> go.Figure:
    fig.update_layout(
        title=title,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=config.COLOR_TEXT),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=20, r=20, t=50, b=20),
    )
    return fig


def emotion_pie_chart(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        fig = go.Figure()
        return _theme_layout(fig, "Emotion Distribution (no data yet)")

    counts = df["emotion"].value_counts().reset_index()
    counts.columns = ["emotion", "count"]
    fig = px.pie(
        counts, names="emotion", values="count", hole=0.45,
        color="emotion", color_discrete_map=config.EMOTION_COLORS,
    )
    return _theme_layout(fig, "Emotion Distribution")


def emotion_bar_chart(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        fig = go.Figure()
        return _theme_layout(fig, "Detections per Emotion (no data yet)")

    counts = df["emotion"].value_counts().reset_index()
    counts.columns = ["emotion", "count"]
    fig = px.bar(
        counts, x="emotion", y="count", color="emotion",
        color_discrete_map=config.EMOTION_COLORS, text="count",
    )
    fig.update_traces(textposition="outside")
    return _theme_layout(fig, "Detections per Emotion")


def emotion_timeline(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        fig = go.Figure()
        return _theme_layout(fig, "Emotion Timeline (no data yet)")

    fig = px.scatter(
        df, x="timestamp", y="emotion", color="emotion",
        color_discrete_map=config.EMOTION_COLORS,
        size="confidence", size_max=12,
        hover_data=["confidence", "song_played"],
    )
    return _theme_layout(fig, "Emotion Timeline")


def summary_stats(df: pd.DataFrame) -> dict:
    if df.empty:
        return {"total": 0, "most_frequent": "—", "avg_confidence": 0.0}
    return {
        "total": len(df),
        "most_frequent": df["emotion"].value_counts().idxmax(),
        "avg_confidence": float(df["confidence"].mean()),
    }


def recent_trend_chart(df: pd.DataFrame, window_seconds: int = 30) -> go.Figure:
    """Line chart of confidence (%) over the last `window_seconds` of detections."""
    fig = go.Figure()
    if df.empty:
        return _theme_layout(fig, f"Live Emotion Trend (last {window_seconds}s)")

    cutoff = df["timestamp"].max() - pd.Timedelta(seconds=window_seconds)
    recent = df[df["timestamp"] >= cutoff]
    if recent.empty:
        recent = df.tail(20)

    fig.add_trace(
        go.Scatter(
            x=recent["timestamp"],
            y=recent["confidence"] * 100,
            mode="lines",
            line=dict(color=config.COLOR_SUCCESS, width=2, shape="spline"),
            fill="tozeroy",
            fillcolor="rgba(0,230,118,0.12)",
        )
    )
    fig.update_yaxes(range=[0, 100], ticksuffix="%")
    fig = _theme_layout(fig, f"Live Emotion Trend (last {window_seconds}s)")
    fig.update_layout(height=220, showlegend=False)
    return fig


def top_emotion_donut(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    if df.empty:
        fig = _theme_layout(fig, "Top Emotion")
        fig.update_layout(height=220)
        return fig

    counts = df["emotion"].value_counts()
    fig.add_trace(
        go.Pie(
            labels=counts.index,
            values=counts.values,
            hole=0.6,
            marker=dict(colors=[config.EMOTION_COLORS.get(e, "#888") for e in counts.index]),
            textinfo="none",
            showlegend=False,
        )
    )
    fig = _theme_layout(fig, "Top Emotion")
    fig.update_layout(height=220, margin=dict(l=10, r=10, t=40, b=10))
    return fig