import pandas as pd
import numpy as np
import statsmodels.api as sm
from pathlib import Path

df = pd.read_csv("data/processed/analysis_sugar_measured.csv")

# --------------------------------------------------
# Prepare predictors
# Reference categories (the "baseline" group):
#   sex: Woman
#   residence: Rural
#   education: No education
#   wealth: Poorest
#   zone: North Central
#   age: continuous (per year)
# --------------------------------------------------

# Dummy variables (drop_first = reference category)
sex_d = pd.get_dummies(df["sex"], prefix="sex", drop_first=True)          # Man
res_d = pd.get_dummies(df["residence_name"], prefix="res", drop_first=True)  # Urban
edu_d = pd.get_dummies(df["education_name"], prefix="edu", drop_first=True)
# force No education as reference
if "edu_No education" in edu_d.columns:
    edu_d = edu_d.drop(columns=["edu_No education"])
# if drop_first dropped something else, rebuild cleanly:
edu_d = pd.get_dummies(df["education_name"], prefix="edu")
edu_d = edu_d.drop(columns=["edu_No education"], errors="ignore")

wealth_d = pd.get_dummies(df["wealth_name"], prefix="wealth")
wealth_d = wealth_d.drop(columns=["wealth_Poorest"], errors="ignore")

zone_d = pd.get_dummies(df["zone_name"], prefix="zone")
zone_d = zone_d.drop(columns=["zone_North Central"], errors="ignore")

# Age as continuous
age = df[["age"]].copy()

# Build X and y
X = pd.concat([age, sex_d, res_d, edu_d, wealth_d, zone_d], axis=1)
X = X.astype(float)
X = sm.add_constant(X)  # intercept
y = df["sugar_measured"].astype(int)

print("Predictors used:")
print(list(X.columns))
print("\nRows in model:", len(y))

# --------------------------------------------------
# Fit logistic regression
# --------------------------------------------------
model = sm.Logit(y, X)
result = model.fit(disp=True)

print("\n" + "=" * 60)
print("LOGISTIC REGRESSION RESULTS")
print("=" * 60)
print(result.summary())

# --------------------------------------------------
# Odds ratios + 95% CI (easier to interpret)
# --------------------------------------------------
params = result.params
conf = result.conf_int()
conf.columns = ["CI_low", "CI_high"]

or_table = pd.DataFrame({
    "odds_ratio": np.exp(params),
    "CI_low": np.exp(conf["CI_low"]),
    "CI_high": np.exp(conf["CI_high"]),
    "p_value": result.pvalues
})
or_table = or_table.round(3)
or_table = or_table.sort_values("odds_ratio", ascending=False)

print("\n" + "=" * 60)
print("ODDS RATIOS (exp(coef))")
print("OR > 1 = higher chance of having been measured")
print("OR < 1 = lower chance")
print("=" * 60)
print(or_table.to_string())

# Save
out = Path("output/tables/logistic_odds_ratios.csv")
or_table.to_csv(out)
print("\nSaved:", out)

# Also save full summary text
with open("output/tables/logistic_summary.txt", "w") as f:
    f.write(result.summary().as_text())
    f.write("\n\nODDS RATIOS\n")
    f.write(or_table.to_string())
print("Saved: output/tables/logistic_summary.txt")