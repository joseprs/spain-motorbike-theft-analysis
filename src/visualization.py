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
    ax[0].set_xticklabels(summary[dimension], rotation=90)

    ax2 = ax[0].twinx()
    ax2.plot(summary[dimension], summary["pct_of_total"], marker="o", linestyle="-")
    ax2.set_ylabel("% of total")

    # Antiquity
    ax[1].bar(summary[dimension], summary["avg_years_to_stole"])
    ax[1].set_title("Average years until theft (antiquity proxy)")
    ax[1].set_xticklabels(summary[dimension], rotation=90)

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
