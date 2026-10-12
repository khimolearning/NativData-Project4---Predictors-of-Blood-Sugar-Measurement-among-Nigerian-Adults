import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

df = pd.read_csv("data/processed/analysis_sugar_measured.csv")

out_dir = Path("output/figures")
out_dir.mkdir(parents=True, exist_ok=True)

def bar_pct(data, col, title, filename, order=None):
    tab = (
        data.groupby(col)["sugar_measured"]
        .mean()
        .mul(100)
        .round(1)
    )
    if order:
        tab = tab.reindex([x for x in order if x in tab.index])
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(tab.index.astype(str), tab.values, color="steelblue", edgecolor="black")
    ax.set_ylabel("% ever had blood sugar measured")
    ax.set_title(title)
    ax.set_ylim(0, max(tab.values) * 1.15)
    plt.xticks(rotation=30, ha="right")
    for bar, val in zip(bars, tab.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f"{val:.1f}%", ha="center", va="bottom", fontsize=9)
    plt.tight_layout()
    path = out_dir / filename
    plt.savefig(path, dpi=150)
    plt.close()
    print("Saved:", path)

# Wealth
bar_pct(
    df, "wealth_name",
    "Blood sugar measurement by wealth quintile (NDHS 2023-24)",
    "sugar_measured_by_wealth.png",
    order=["Poorest", "Poorer", "Middle", "Richer", "Richest"]
)

# Zone
bar_pct(
    df, "zone_name",
    "Blood sugar measurement by geopolitical zone (NDHS 2023-24)",
    "sugar_measured_by_zone.png",
    order=["North Central", "North East", "North West", "South East", "South South", "South West"]
)

# Education
bar_pct(
    df, "education_name",
    "Blood sugar measurement by education (NDHS 2023-24)",
    "sugar_measured_by_education.png",
    order=["No education", "Primary", "Secondary", "Higher"]
)

print("Done.")