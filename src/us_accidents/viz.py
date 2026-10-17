"""Interactive Plotly figures."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from . import analysis

TEMPLATE = "plotly_white"


def severity_chart(df: pd.DataFrame) -> go.Figure:
    data = analysis.severity_distribution(df).reset_index().rename(columns={"index": "Severity"})
    fig = px.bar(data, x="Severity", y="accidents", text="share_pct", template=TEMPLATE,
                 title="Accidents by severity (1 = least impact, 4 = most impact)")
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    return fig


def hourly_chart(df: pd.DataFrame) -> go.Figure:
    data = analysis.accidents_by_hour(df)
    fig = px.line(data, x=data.index, y=data.columns, markers=True, template=TEMPLATE,
                  title="Accidents by hour of day: weekdays vs. weekends",
                  labels={"x": "Hour of day", "value": "Accidents", "variable": ""})
    return fig


def weekday_chart(df: pd.DataFrame) -> go.Figure:
    data = analysis.accidents_by_weekday(df)
    return px.bar(x=data.index, y=data.values, template=TEMPLATE, title="Accidents by weekday",
                  labels={"x": "", "y": "Accidents"})


def monthly_chart(df: pd.DataFrame) -> go.Figure:
    data = analysis.accidents_by_month(df)
    return px.bar(x=data.index, y=data.values, template=TEMPLATE, title="Accidents by month",
                  labels={"x": "Month", "y": "Accidents"})


def top_states_chart(df: pd.DataFrame, n: int = 15) -> go.Figure:
    data = analysis.top_values(df, "State", n).reset_index().rename(columns={"index": "State"})
    return px.bar(data, x="State", y="accidents", template=TEMPLATE, title=f"Top {n} states by accidents")


def weather_chart(df: pd.DataFrame, n: int = 12) -> go.Figure:
    data = analysis.top_values(df, "Weather_Condition", n).reset_index()
    data = data.rename(columns={data.columns[0]: "Weather_Condition"})
    return px.bar(data, x="accidents", y="Weather_Condition", orientation="h", template=TEMPLATE,
                  title=f"Top {n} weather conditions").update_yaxes(autorange="reversed")


def road_features_chart(df: pd.DataFrame) -> go.Figure:
    data = analysis.road_feature_rates(df).reset_index().rename(columns={"index": "Feature"})
    return px.bar(data, x="share_pct", y="Feature", orientation="h", template=TEMPLATE,
                  title="Share of accidents near each road feature (%)").update_yaxes(autorange="reversed")


def map_chart(df: pd.DataFrame, max_points: int = 20_000) -> go.Figure | None:
    if not {"Start_Lat", "Start_Lng"} <= set(df.columns):
        return None
    sample = df.sample(min(max_points, len(df)), random_state=42)
    return px.scatter_geo(sample, lat="Start_Lat", lon="Start_Lng", color="Severity", scope="usa",
                          template=TEMPLATE, opacity=0.5, title="Accident locations (random sample)")


FIGURES = {
    "severity": severity_chart,
    "by_hour": hourly_chart,
    "by_weekday": weekday_chart,
    "by_month": monthly_chart,
    "top_states": top_states_chart,
    "weather": weather_chart,
    "road_features": road_features_chart,
    "map": map_chart,
}
