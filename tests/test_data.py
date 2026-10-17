import pandas as pd
import pytest

from us_accidents.data import clean_accidents, load_accidents


def test_clean_removes_duplicates_and_bad_dates(raw_df):
    clean = clean_accidents(raw_df)
    assert clean["ID"].is_unique
    assert "A-bad" not in set(clean["ID"])
    assert len(clean) == 600 + 1  # 600 originals + the negative-duration row (kept, duration NaN)


def test_negative_duration_becomes_nan(raw_df):
    clean = clean_accidents(raw_df)
    assert pd.isna(clean.loc[clean["ID"] == "A-neg", "Duration_min"]).all()
    assert (clean["Duration_min"].dropna() > 0).all()


def test_columns_are_renamed_and_features_added(raw_df):
    clean = clean_accidents(raw_df)
    assert {"Traffic_Message_Channel", "Street_Number"} <= set(clean.columns)
    assert {"Year", "Month", "Hour", "Weekday", "Is_Weekend"} <= set(clean.columns)
    assert clean["Hour"].between(0, 23).all()
    assert clean["Severity"].between(1, 4).all()


def test_load_accidents_nrows(csv_path):
    assert len(load_accidents(csv_path, nrows=50)) == 50


def test_load_accidents_sample_is_reproducible(csv_path):
    a = load_accidents(csv_path, sample_frac=0.3, seed=1)
    b = load_accidents(csv_path, sample_frac=0.3, seed=1)
    assert a.equals(b)
    assert 0 < len(a) < 603


def test_load_requires_core_columns(tmp_path):
    path = tmp_path / "bad.csv"
    pd.DataFrame({"foo": [1]}).to_csv(path, index=False)
    with pytest.raises(ValueError, match="missing required columns"):
        load_accidents(path)


def test_invalid_sample_frac(csv_path):
    with pytest.raises(ValueError):
        load_accidents(csv_path, sample_frac=1.5)
