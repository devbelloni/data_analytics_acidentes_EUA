"""Aggregations used by the report. Every function is pure: DataFrame in, DataFrame out."""

from __future__ import annotations

import pandas as pd

from .config import ROAD_FEATURES, WEATHER_COLUMNS, WEEKDAYS


def severity_distribution(df: pd.DataFrame) -> pd.DataFrame:
    counts = df["Severity"].value_counts().sort_index()
    return pd.DataFrame({"accidents": counts, "share_pct": (counts / counts.sum() * 100).round(2)})


def accidents_by_hour(df: pd.DataFrame) -> pd.DataFrame:
    by_hour = df.groupby(["Hour", "Is_Weekend"], observed=True).size().unstack(fill_value=0)
    by_hour.columns = ["weekday" if not c else "weekend" for c in by_hour.columns]
    return by_hour.reindex(range(24), fill_value=0)


def accidents_by_weekday(df: pd.DataFrame) -> pd.Series:
    return df["Weekday"].value_counts().reindex(WEEKDAYS, fill_value=0)


def accidents_by_month(df: pd.DataFrame) -> pd.Series:
    return df["Month"].value_counts().sort_index()


def top_values(df: pd.DataFrame, column: str, n: int = 10) -> pd.DataFrame:
    """Most frequent values of ``column`` with their share of all accidents."""
    if column not in df:
        return pd.DataFrame(columns=["accidents", "share_pct"])
    counts = df[column].value_counts().head(n)
    return pd.DataFrame({"accidents": counts, "share_pct": (counts / len(df) * 100).round(2)})


def mean_severity_by(df: pd.DataFrame, column: str, min_count: int = 30) -> pd.DataFrame:
    """Average severity per group, ignoring groups with fewer than ``min_count`` accidents."""
    grouped = df.groupby(column, observed=True)["Severity"].agg(["mean", "count"])
    return grouped[grouped["count"] >= min_count].sort_values("mean", ascending=False).round(3)


def duration_by_severity(df: pd.DataFrame) -> pd.DataFrame:
    if "Duration_min" not in df:
        return pd.DataFrame()
    return (
        df.groupby("Severity")["Duration_min"]
        .describe(percentiles=[0.5, 0.9])[["count", "mean", "50%", "90%"]]
        .rename(columns={"50%": "median", "90%": "p90"})
        .round(1)
    )


def road_feature_rates(df: pd.DataFrame) -> pd.DataFrame:
    """Share of accidents that occurred at a location flagged with each road feature."""
    present = [c for c in ROAD_FEATURES if c in df]
    rates = (df[present].mean() * 100).round(2).sort_values(ascending=False)
    return rates.rename("share_pct").to_frame()


def weather_summary(df: pd.DataFrame) -> pd.DataFrame:
    present = [c for c in WEATHER_COLUMNS if c in df]
    return df[present].describe().T[["count", "mean", "min", "50%", "max"]].round(2)


def missing_report(df: pd.DataFrame) -> pd.DataFrame:
    missing = df.isna().sum()
    report = pd.DataFrame({"missing": missing, "missing_pct": (missing / len(df) * 100).round(2)})
    return report[report["missing"] > 0].sort_values("missing", ascending=False)
