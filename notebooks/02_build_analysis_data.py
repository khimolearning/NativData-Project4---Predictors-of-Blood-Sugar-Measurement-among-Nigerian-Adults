import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 1. Load
# --------------------------------------------------
women = pd.read_csv("data/processed/women_ncd_key_vars.csv")
men = pd.read_csv("data/processed/men_ncd_key_vars.csv")

# --------------------------------------------------
# 2. Keep only the columns we need + rename
# --------------------------------------------------
women_df = women[["v024", "v025", "v012", "v106", "v190", "chd06"]].copy()
women_df = women_df.rename(columns={
    "v024": "zone",
    "v025": "residence",
    "v012": "age",
    "v106": "education",
    "v190": "wealth",
    "chd06": "sugar_measured"
})
women_df["sex"] = "Woman"

men_df = men[["mv024", "mv025", "mv012", "mv106", "mv190", "mchd06"]].copy()
men_df = men_df.rename(columns={
    "mv024": "zone",
    "mv025": "residence",
    "mv012": "age",
    "mv106": "education",
    "mv190": "wealth",
    "mchd06": "sugar_measured"
})
men_df["sex"] = "Man"

# --------------------------------------------------
# 3. Combine
# --------------------------------------------------
df = pd.concat([women_df, men_df], ignore_index=True)

print("Combined shape:", df.shape)
print("\nSugar measured value counts (before cleaning):")
print(df["sugar_measured"].value_counts(dropna=False))

# --------------------------------------------------
# 4. Clean outcome
# DHS often uses: 0 = No, 1 = Yes, 8 = Don't know
# We keep only clear Yes/No
# --------------------------------------------------
df = df[df["sugar_measured"].isin([0, 1])].copy()
df["sugar_measured"] = df["sugar_measured"].astype(int)

print("\nSugar measured after cleaning (0=No, 1=Yes):")
print(df["sugar_measured"].value_counts())
print("Percent Yes: {:.1f}%".format(100 * df["sugar_measured"].mean()))

# --------------------------------------------------
# 5. Friendly labels (for tables later)
# --------------------------------------------------
zone_map = {
    1: "North Central",
    2: "North East",
    3: "North West",
    4: "South East",
    5: "South South",
    6: "South West"
}
residence_map = {1: "Urban", 2: "Rural"}
# DHS education: often 0=None, 1=Primary, 2=Secondary, 3=Higher
education_map = {0: "No education", 1: "Primary", 2: "Secondary", 3: "Higher"}
# Wealth quintile 1-5
wealth_map = {1: "Poorest", 2: "Poorer", 3: "Middle", 4: "Richer", 5: "Richest"}

df["zone_name"] = df["zone"].map(zone_map)
df["residence_name"] = df["residence"].map(residence_map)
df["education_name"] = df["education"].map(education_map)
df["wealth_name"] = df["wealth"].map(wealth_map)

# Age groups (useful for tables)
df["age_group"] = pd.cut(
    df["age"],
    bins=[14, 24, 34, 44, 59],
    labels=["15-24", "25-34", "35-44", "45-59"]
)

print("\n--- Preview ---")
print(df.head(10))
print("\nMissing in key columns:")
print(df[["sugar_measured", "age", "sex", "residence", "education", "wealth", "zone"]].isnull().sum())

# --------------------------------------------------
# 6. Save
# --------------------------------------------------
out_path = Path("data/processed/analysis_sugar_measured.csv")
df.to_csv(out_path, index=False)
print("\nSaved:", out_path)
print("Final rows:", len(df))