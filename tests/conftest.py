"""Synthetic data that mimics the structure of the real CSV (never the real values)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest


def make_raw(n: int = 600, seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    start = pd.Timestamp("2021-01-01") + pd.to_timedelta(rng.integers(0, 365 * 24 * 60, n), unit="m")
    duration = pd.to_timedelta(rng.integers(5, 240, n), unit="m")
    df = pd.DataFrame(
        {
            "ID": [f"A-{i}" for i in range(n)],
            "Severity": rng.choice([1, 2, 3, 4], n, p=[0.05, 0.7, 0.2, 0.05]),
            "Start_Time": start.astype(str),
            "End_Time": (start + duration).astype(str),
            "Start_Lat": rng.uniform(25, 48, n),
            "Start_Lng": rng.uniform(-123, -70, n),
            "City": rng.choice(["Austin", "Miami", "Denver", "Boston"], n),
            "State": rng.choice(["TX", "FL", "CO", "MA"], n),
            "Weather_Condition": rng.choice(["Clear", "Rain", "Fog", "Snow", None], n),
            "Temperature(F)": rng.normal(60, 15, n),
            "TMC": rng.choice([201.0, 241.0, np.nan], n),
            "Number": rng.choice([100.0, np.nan], n),
            "Crossing": rng.random(n) < 0.1,
            "Junction": rng.random(n) < 0.15,
            "Traffic_Signal": rng.random(n) < 0.2,
        }
    )
    return df


@pytest.fixture
def raw_df() -> pd.DataFrame:
    df = make_raw()
    # Dirty rows a real export contains: a duplicate, a bad date, a negative duration.
    dup = df.iloc[[0]].copy()
    bad_date = df.iloc[[1]].copy().assign(ID="A-bad", Start_Time="not a date")
    negative = df.iloc[[2]].copy().assign(ID="A-neg", End_Time="2000-01-01 00:00:00")
    return pd.concat([df, dup, bad_date, negative], ignore_index=True)


@pytest.fixture
def csv_path(tmp_path, raw_df):
    path = tmp_path / "accidents.csv"
    raw_df.to_csv(path, index=False)
    return path
