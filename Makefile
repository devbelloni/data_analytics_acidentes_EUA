CSV ?= data/raw/US_Accidents_Dec21_updated.csv

.PHONY: install test lint report
install:
	pip install -e ".[dev]"
test:
	pytest -q
lint:
	ruff check .
report:
	python -m us_accidents.report $(CSV) --sample-frac 0.1
