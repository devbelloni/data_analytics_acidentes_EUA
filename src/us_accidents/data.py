"""Loading and cleaning of the US Accidents CSV."""

from __future__ import annotations

import random
from pathlib import Path

import numpy as np
import pandas as pd

from .config import MAX_DURATION_MIN, RENAMES, REQUIRED_COLUMNS, ROAD_FEATURES, USECOLS, WEEKDAYS


def load_accidents(
    path: str | Path,
    nrows: int | None = None,
    sample_frac: float | None = None,
    seed: int = 42,
) -> pd.DataFrame:
    """Read the raw CSV, keeping only the analysis columns.

    Parameters
    ----------
    nrows:
        Read only the first ``nrows`` rows (fast smoke runs).
    sample_frac:
        Read a random fraction of rows while streaming the file, so the full multi-GB
        CSV never has to fit in memory. Ignored when ``nrows`` is given.
    """
    path = Path(path)
    header = pd.read_csv(path, nrows=0).columns
    missing = [c for c in REQUIRED_COLUMNS if c not in header]
    if missing:
        raise ValueError(f"{path} is missing required columns: {missing}")
    usecols = [c for c in USECOLS if c in header]
    # TMC and Number are only renamed (not analysed), so they are read when present.
    usecols += [c for c in RENAMES if c in header and c not in usecols]

    skiprows = None
    if sample_frac is not None and nrows is None:
        if not 0 < sample_frac <= 1:
            raise ValueError("sample_frac must be in (0, 1]")
        rng = random.Random(seed)
        skiprows = lambda i: i > 0 and rng.random() > sample_frac  # noqa: E731

    return pd.read_csv(path, usecols=usecols, nrows=nrows, skiprows=skiprows)


def clean_accidents(df: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned copy with parsed dates, durations and calendar features."""
    out = df.copy()

    if "ID" in out:
        out = out.drop_duplicates(subset="ID")
    else:
        out = out.drop_duplicates()

    out = out.rename(columns={k: v for k, v in RENAMES.items() if k in out})

    out["Start_Time"] = pd.to_datetime(out["Start_Time"], errors="coerce", format="mixed")
    if "End_Time" in out:
        out["End_Time"] = pd.to_datetime(out["End_Time"], errors="coerce", format="mixed")
    out["Severity"] = pd.to_numeric(out["Severity"], errors="coerce")
    out = out.dropna(subset=["Start_Time", "Severity"]).copy()
    out["Severity"] = out["Severity"].astype(int)

    if "End_Time" in out:
        duration = (out["End_Time"] - out["Start_Time"]).dt.total_seconds() / 60
        out["Duration_min"] = duration.where((duration > 0) & (duration <= MAX_DURATION_MIN))

    start = out["Start_Time"]
    out["Year"] = start.dt.year
    out["Month"] = start.dt.month
    out["Hour"] = start.dt.hour
    out["Weekday"] = pd.Categorical(start.dt.day_name(), categories=WEEKDAYS, ordered=True)
    out["Is_Weekend"] = start.dt.dayofweek >= 5

    for col in ROAD_FEATURES:
        if col in out:
            out[col] = out[col].astype(bool)

    return out.reset_index(drop=True)


def memory_mb(df: pd.DataFrame) -> float:
    """Deep memory footprint of a DataFrame in megabytes."""
    return float(np.round(df.memory_usage(deep=True).sum() / 1024**2, 2))
