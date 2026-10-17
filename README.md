# US Road Accidents: Exploratory Data Analysis

Exploratory analysis of the **US Accidents** dataset (traffic accidents across the United
States), focused on data preparation and interactive visualization with Plotly.

## What the script does

- Loads the first 100,000 records of the dataset
- Removes duplicates and renames ambiguous columns
- Converts `Start_Time` and `End_Time` to datetime
- Profiles missing values per column
- Builds interactive Plotly charts

## Data

The dataset is not included (it is large). Download it from Kaggle:
[US Accidents (Sobhan Moosavi)](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents)
and place `US_Accidents_Dec21_updated.csv` next to `main.py`.

## Run it

```bash
pip install -r requirements.txt
python main.py
```

## Stack

Python, pandas, Plotly.

## Author

**Márcio Belloni**, AI/ML Engineer.
[LinkedIn](https://www.linkedin.com/in/marcio-belloni/) · [GitHub](https://github.com/devbelloni)
