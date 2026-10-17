from us_accidents.report import main


def test_cli_generates_summary_and_figures(csv_path, tmp_path):
    out = tmp_path / "reports"
    assert main([str(csv_path), "--out", str(out)]) == 0
    summary = (out / "summary.md").read_text(encoding="utf-8")
    assert "Severity distribution" in summary
    assert "Top 10 states" in summary
    figures = {p.stem for p in (out / "figures").glob("*.html")}
    assert {"severity", "by_hour", "by_weekday", "top_states", "map"} <= figures
