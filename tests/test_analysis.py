import pytest

from us_accidents import analysis
from us_accidents.data import clean_accidents


@pytest.fixture
def df(raw_df):
    return clean_accidents(raw_df)


def test_severity_distribution_sums_to_100(df):
    dist = analysis.severity_distribution(df)
    assert dist["accidents"].sum() == len(df)
    assert dist["share_pct"].sum() == pytest.approx(100, abs=0.1)


def test_hourly_has_24_rows_and_all_accidents(df):
    hourly = analysis.accidents_by_hour(df)
    assert list(hourly.index) == list(range(24))
    assert hourly.to_numpy().sum() == len(df)


def test_weekday_order_and_total(df):
    wd = analysis.accidents_by_weekday(df)
    assert list(wd.index)[0] == "Monday" and list(wd.index)[-1] == "Sunday"
    assert wd.sum() == len(df)


def test_top_values_and_missing_column(df):
    assert len(analysis.top_values(df, "State", 3)) == 3
    assert analysis.top_values(df, "does_not_exist").empty


def test_mean_severity_respects_min_count(df):
    assert analysis.mean_severity_by(df, "State", min_count=10**6).empty


def test_road_feature_rates_are_percentages(df):
    rates = analysis.road_feature_rates(df)["share_pct"]
    assert rates.between(0, 100).all()


def test_missing_report_flags_weather_gaps(df):
    assert "Weather_Condition" in analysis.missing_report(df).index
