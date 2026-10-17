"""Command-line entry point: builds figures and a Markdown summary from the raw CSV.

Example::

    python -m us_accidents.report data/raw/US_Accidents_Dec21_updated.csv --sample-frac 0.1
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from . import analysis, viz
from .data import clean_accidents, load_accidents, memory_mb


def _md(title: str, table: pd.DataFrame | pd.Series) -> str:
    if table is None or len(table) == 0:
        return ""
    return f"## {title}\n\n{table.to_markdown()}\n\n"


def build_summary(df: pd.DataFrame, source: str) -> str:
    start, end = df["Start_Time"].min(), df["Start_Time"].max()
    weather_severity = (
        analysis.mean_severity_by(df, "Weather_Condition").head(10) if "Weather_Condition" in df else None
    )
    parts = [
        "# US Accidents: analysis summary\n\n",
        f"- **Source file:** `{source}`\n",
        f"- **Records analysed:** {len(df):,} ({memory_mb(df)} MB in memory)\n",
        f"- **Period:** {start:%Y-%m-%d} to {end:%Y-%m-%d}\n\n",
        _md("Severity distribution", analysis.severity_distribution(df)),
        _md("Accident duration by severity (minutes)", analysis.duration_by_severity(df)),
        _md("Top 10 states", analysis.top_values(df, "State", 10)),
        _md("Top 10 cities", analysis.top_values(df, "City", 10)),
        _md("Top 10 weather conditions", analysis.top_values(df, "Weather_Condition", 10)),
        _md("Mean severity by weather condition (min. 30 accidents)", weather_severity),
        _md("Share of accidents near road features (%)", analysis.road_feature_rates(df)),
        _md("Weather variables", analysis.weather_summary(df)),
        _md("Columns with missing values", analysis.missing_report(df)),
    ]
    return "".join(parts)


def run(csv: Path, out: Path, nrows: int | None, sample_frac: float | None, seed: int) -> Path:
    raw = load_accidents(csv, nrows=nrows, sample_frac=sample_frac, seed=seed)
    df = clean_accidents(raw)
    figures_dir = out / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    for name, builder in viz.FIGURES.items():
        fig = builder(df)
        if fig is not None:
            fig.write_html(figures_dir / f"{name}.html", include_plotlyjs="cdn")
    summary = out / "summary.md"
    summary.write_text(build_summary(df, csv.name), encoding="utf-8")
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("csv", type=Path, help="Path to US_Accidents_*.csv")
    parser.add_argument("--out", type=Path, default=Path("reports"), help="Output directory")
    parser.add_argument("--nrows", type=int, default=None, help="Read only the first N rows")
    parser.add_argument("--sample-frac", type=float, default=None, help="Random fraction of rows (0-1]")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args(argv)
    summary = run(args.csv, args.out, args.nrows, args.sample_frac, args.seed)
    print(f"Report written to {summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
