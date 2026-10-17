# US Accidents: Exploratory Analysis Toolkit

![CI](https://github.com/devbelloni/data_analytics_acidentes_EUA/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A reproducible pipeline for exploring the **US Accidents** dataset, a countrywide traffic
accident dataset with millions of records. It loads the raw CSV efficiently, cleans it, and
produces a Markdown summary plus interactive Plotly figures with one command.

The goal is to answer practical questions: *When do accidents happen? Where? Under which
weather and road conditions? How severe are they and how long do they block traffic?*

## Features

- **Memory-safe loading:** reads only the needed columns and can stream a random sample
  (`--sample-frac`) or the first rows (`--nrows`) so the multi-GB file never has to fit in memory.
- **Documented cleaning:** de-duplication by `ID`, robust date parsing, derived calendar
  features, accident duration with invalid values removed, and renamed ambiguous columns.
- **Pure analysis functions** (`analysis.py`): severity, hour, weekday and month patterns,
  top states, cities and weather conditions, road-feature rates, duration by severity and a
  missing-value report.
- **Interactive figures** (`viz.py`): eight Plotly charts exported as standalone HTML,
  including a map of accident locations.
- **Tested and linted:** 15 pytest tests on synthetic data, `ruff` and a GitHub Actions
  workflow on Python 3.10, 3.11 and 3.12.

## Quick start

```bash
git clone https://github.com/devbelloni/data_analytics_acidentes_EUA.git
cd data_analytics_acidentes_EUA
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

### 1. Get the data

The dataset is not included (about 1 GB). Download it from Kaggle,
[US Accidents (Sobhan Moosavi)](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents),
and place the CSV in `data/raw/`:

```bash
kaggle datasets download -d sobhanmoosavi/us-accidents -p data/raw --unzip
```

### 2. Generate the report

```bash
# 10% random sample (fast)
python -m us_accidents.report data/raw/US_Accidents_Dec21_updated.csv --sample-frac 0.1

# or the full file / the first 100,000 rows
python -m us_accidents.report data/raw/US_Accidents_Dec21_updated.csv
python -m us_accidents.report data/raw/US_Accidents_Dec21_updated.csv --nrows 100000
```

Output (in `reports/`, git-ignored):

- `summary.md`: severity distribution, durations, rankings, road features, weather and
  missing-value tables
- `figures/*.html`: interactive charts (severity, hour of day, weekday, month, states,
  weather conditions, road features, map)

`make report` runs the 10% sample with the default file name.

## Method and cleaning decisions

| Step | Decision | Why |
|---|---|---|
| Columns | Read only the analysis subset of the CSV | Cuts memory use and load time |
| Duplicates | Drop by `ID` | `ID` is the record key |
| Dates | `pd.to_datetime(..., errors="coerce", format="mixed")`, drop rows with invalid start time | Timestamps mix formats (with and without fractional seconds) |
| Duration | `End_Time - Start_Time` in minutes; non-positive or longer than 7 days becomes missing | Those values are data-entry errors, not real durations |
| Renames | `TMC` to `Traffic_Message_Channel`, `Number` to `Street_Number` | The original names are ambiguous |
| Features | `Year`, `Month`, `Hour`, ordered `Weekday`, `Is_Weekend` | Needed for time-pattern analysis |
| Severity by group | Groups with fewer than 30 accidents are ignored | Avoids noisy averages from tiny groups |

## Project structure

```
.
├── src/us_accidents/
│   ├── config.py      # column lists and constants
│   ├── data.py        # loading and cleaning
│   ├── analysis.py    # pure aggregation functions
│   ├── viz.py         # Plotly figures
│   └── report.py      # CLI entry point
├── tests/             # pytest suite on synthetic data
├── data/raw/          # place the CSV here (git-ignored)
├── reports/           # generated output (git-ignored)
├── .github/workflows/ci.yml
├── Makefile
└── pyproject.toml
```

## Development

```bash
make test     # pytest
make lint     # ruff
```

The tests use synthetic data that mimics the structure of the real file, so they run
without downloading anything and cover cleaning, aggregation and the command-line report.

## Data source and citation

The data comes from the US Accidents dataset by Sobhan Moosavi et al.; please check the
Kaggle page for its license and terms of use before redistributing derived data.

- Moosavi, S., Samavatian, M. H., Parthasarathy, S., and Ramnath, R. *A Countrywide Traffic
  Accident Dataset*, 2019.
- Moosavi, S., Samavatian, M. H., Parthasarathy, S., Teodorescu, R., and Ramnath, R.
  *Accident Risk Prediction based on Heterogeneous Sparse Data: New Dataset and Insights*,
  ACM SIGSPATIAL, 2019.

## Author

**Márcio Belloni**, AI/ML Engineer.
[LinkedIn](https://www.linkedin.com/in/marcio-belloni/) · [GitHub](https://github.com/devbelloni)

## License

MIT, see [LICENSE](LICENSE). The dataset has its own license.
