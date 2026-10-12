import pandas as pd
from pathlib import Path

# Paths
women_path = Path("data/processed/women_ncd_key_vars.csv")
men_path = Path("data/processed/men_ncd_key_vars.csv")

print("=" * 60)
print("WOMEN FILE")
print("=" * 60)
women = pd.read_csv(women_path)
print("Shape (rows, columns):", women.shape)
print("\nColumn names:")
print(list(women.columns))
print("\nFirst 5 rows:")
print(women.head())
print("\nMissing values per column:")
print(women.isnull().sum())

print("\n" + "=" * 60)
print("MEN FILE")
print("=" * 60)
men = pd.read_csv(men_path)
print("Shape (rows, columns):", men.shape)
print("\nColumn names:")
print(list(men.columns))
print("\nFirst 5 rows:")
print(men.head())
print("\nMissing values per column:")
print(men.isnull().sum())