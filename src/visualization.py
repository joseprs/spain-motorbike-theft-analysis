from __future__ import annotations

import pandas as pd
import matplotlib.pyplot as plt


def bar_plot(x, y, title: str, xlabel: str = "", ylabel: str = ""):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(x, y)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()


def plot_total_share_and_antiquity(summary: pd.DataFrame, dimension: str):
    """
    Two-row plot:
    - total stolen (bars) + % of total (line)
    - avg years_to_stole (bars)
    """
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(12, 8))

    # Total + share
    ax[0].bar(summary[dimension], summary["stolen_total"])
    ax[0].set_title(f"Total stolen by {dimension} + share of total")
    ax[0].tick_params(axis="x", rotation=90)

    ax2 = ax[0].twinx()
    ax2.plot(summary[dimension], summary["pct_of_total"], marker="o", linestyle="-")
    ax2.set_ylabel("% of total")

    # Antiquity
    ax[1].bar(summary[dimension], summary["avg_years_to_stole"])
    ax[1].set_title("Average years until theft (antiquity proxy)")
    ax[1].tick_params(axis="x", rotation=90)

    plt.tight_layout()
    plt.show()


def plot_count_and_growth_by_year(df_year: pd.DataFrame) -> None:
    """
    Bar chart for counts + line chart for YoY growth (%).
    Expects columns: stolen_year, count, growth_pct
    """

    fig, ax1 = plt.subplots(figsize=(12, 5))

    ax1.bar(df_year["stolen_year"], df_year["count"], alpha=0.35, label="Count")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Count of stolen items")

    ax2 = ax1.twinx()
    ax2.plot(df_year["stolen_year"], df_year["growth_pct"], marker="o", linestyle="-", label="Growth %")
    ax2.set_ylabel("Percentage growth (%)")

    ax1.set_title("Stolen motorbikes count and percentage growth by year")
    plt.tight_layout()
    plt.show()


def plot_year_comparison_and_growth(summary: pd.DataFrame,dimension: str,year1: int,year2: int,reliable_only: bool = True):
    data = summary.copy()
    if reliable_only:
        data = data[data["is_growth_reliable"]]

    x = range(len(data))
    fig, ax1 = plt.subplots(figsize=(14, 6))

    ax1.bar([i - 0.2 for i in x], data[f"stolen_{year1}"], width=0.4, label=str(year1))
    ax1.bar([i + 0.2 for i in x], data[f"stolen_{year2}"], width=0.4, label=str(year2))
    ax1.set_xticks(list(x))
    ax1.set_xticklabels(data[dimension], rotation=45)
    ax1.set_ylabel("Stolen vehicles")
    ax1.set_title(f"Stolen vehicles by {dimension}: {year1} vs {year2} + growth")
    ax1.legend(loc="upper left")

    ax2 = ax1.twinx()
    ax2.plot(list(x), data["growth_pct"], marker="o", linestyle="-", label="Growth %")
    ax2.set_ylabel("Growth %")
    ax2.legend(loc="upper right")

    plt.tight_layout()
    plt.show()


def plot_antiquity_histogram(df, column="years_to_stole", bins=40, reference="median") -> None:
    """
    Histogram of vehicle age at theft. Optionally draws a reference line (median or mean).
    """
    import matplotlib.pyplot as plt

    values = df[column].dropna()
    ref_value = values.median() if reference == "median" else values.mean()

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.hist(values, bins=bins, alpha=0.75)
    ax.axvline(ref_value, linestyle="--", linewidth=2)
    ax.set_title("Years from registration to theft (antiquity proxy)")
    ax.set_xlabel("Years")
    ax.set_ylabel("Stolen motorbikes")
    plt.tight_layout()
    plt.show()


def plot_top_rates(df: pd.DataFrame, dimension: str, rate_col: str, top_n: int = 20) -> None:
    data = df.sort_values(rate_col, ascending=False).head(top_n)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(data[dimension], data[rate_col])
    ax.set_title(f"Top {top_n} provinces by theft rate")
    ax.set_ylabel("Thefts per 100,000 inhabitants")
    ax.set_xticklabels(data[dimension], rotation=90)

    plt.tight_layout()
    plt.show()