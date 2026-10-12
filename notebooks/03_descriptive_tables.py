import pandas as pd
from pathlib import Path

df = pd.read_csv("data/processed/analysis_sugar_measured.csv")

def screening_table(data, col, label):
    """Percent who ever had blood sugar measured, by group"""
    tab = (
        data.groupby(col, dropna=False)
        .agg(
            n=("sugar_measured", "size"),
            n_measured=("sugar_measured", "sum"),
            pct_measured=("sugar_measured", "mean")
        )
        .reset_index()
    )
    tab["pct_measured"] = (100 * tab["pct_measured"]).round(1)
    tab = tab.rename(columns={col: label})
    return tab

print("=" * 60)
print("OVERALL")
print("=" * 60)
print(f"Total adults: {len(df):,}")
print(f"Ever had blood sugar measured: {df['sugar_measured'].sum():,} ({100*df['sugar_measured'].mean():.1f}%)")

print("\n" + "=" * 60)
print("BY SEX")
print("=" * 60)
print(screening_table(df, "sex", "Sex").to_string(index=False))

print("\n" + "=" * 60)
print("BY RESIDENCE")
print("=" * 60)
print(screening_table(df, "residence_name", "Residence").to_string(index=False))

print("\n" + "=" * 60)
print("BY EDUCATION")
print("=" * 60)
print(screening_table(df, "education_name", "Education").to_string(index=False))

print("\n" + "=" * 60)
print("BY WEALTH")
print("=" * 60)
print(screening_table(df, "wealth_name", "Wealth").to_string(index=False))

print("\n" + "=" * 60)
print("BY ZONE")
print("=" * 60)
print(screening_table(df, "zone_name", "Zone").to_string(index=False))

print("\n" + "=" * 60)
print("BY AGE GROUP")
print("=" * 60)
print(screening_table(df, "age_group", "Age group").to_string(index=False))

# Save one combined summary for the report
tables = {
    "sex": screening_table(df, "sex", "group"),
    "residence": screening_table(df, "residence_name", "group"),
    "education": screening_table(df, "education_name", "group"),
    "wealth": screening_table(df, "wealth_name", "group"),
    "zone": screening_table(df, "zone_name", "group"),
    "age_group": screening_table(df, "age_group", "group"),
}

out = Path("output/tables/descriptive_screening_rates.xlsx")
with pd.ExcelWriter(out, engine="openpyxl") as writer:
    for name, tab in tables.items():
        tab.to_excel(writer, sheet_name=name, index=False)
print("\nSaved Excel:", out)