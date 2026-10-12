# NativData Project 4 — Predictors of Blood Sugar Measurement (NDHS 2023-24)

**Question:** Which factors are associated with whether an adult in Nigeria has ever had their blood sugar measured?

**Short answer:** Wealth and education are the strongest factors. The poorest and those with no education are far less likely to have been screened. Southern zones have higher rates than North Central. After adjustment, urban residence alone is not a clear driver.

## Why this project
Nigeria’s overall blood-sugar measurement rate in the NDHS 2023-24 is low (\~19.5%). This analysis shows *who* is being missed. The results can help prioritise limited screening resources.

## Method
- Data: NDHS 2023-24 (women and men)
- Descriptive rates by group
- Logistic regression (odds ratios) adjusting for age, sex, residence, education, wealth, and zone

## Main result (adjusted odds ratios)
| Comparison | Odds ratio |
|------------|------------|
| Richest vs poorest | 5.1 |
| Higher education vs none | 3.7 |
| South South vs North Central | 1.9 |
| Age (per year) | 1.07 |

## Folder structure
- `data/processed/` — analysis dataset
- `notebooks/` — scripts (01 to 05)
- `output/tables/` — descriptive and model tables
- `output/figures/` — charts

## How to reproduce
```bash
uv venv
.venv\Scripts\activate
uv add pandas numpy pyreadstat statsmodels scikit-learn matplotlib seaborn openpyxl
python notebooks/01_inspect_data.py
python notebooks/02_build_analysis_data.py
python notebooks/03_descriptive_tables.py
python notebooks/04_logistic_regression.py
python notebooks/05_charts.py