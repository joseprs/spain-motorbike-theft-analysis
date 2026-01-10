from __future__ import annotations

import numpy as np
import pandas as pd


def thefts_by_month(df: pd.DataFrame) -> pd.DataFrame:
    out = df.groupby("stolen_month").size().reset_index(name="count").sort_values("stolen_month")
    return out


def thefts_by_weekday(df: pd.DataFrame) -> pd.DataFrame:
    out = df.groupby(["stolen_weekday", "stolen_weekday_name"]).size().reset_index(name="count").sort_values("stolen_weekday")
    return out


def summary_by_dimension(df: pd.DataFrame, dimension: str, years_for_growth: tuple[int, int] = (2021, 2022), end_date_mmdd: str = "11-30", min_count_growth: int = 10) -> pd.DataFrame:
    """
    Returns a table with:
    - total stolen count
    - % of all stolen
    - avg years_to_stole
    - stolen counts for year1/year2 (up to end_date_mmdd)
    - growth %
    """
    year1, year2 = years_for_growth

    # Total + avg antiquity
    base = (
        df.groupby(dimension)["years_to_stole"]
        .agg(stolen_total="count", avg_years_to_stole="mean")
        .reset_index()
    )
    base["pct_of_total"] = base["stolen_total"] / base["stolen_total"].sum() * 100

    # Year filters (comparing same cut-off date)
    cutoff1 = pd.to_datetime(f"{year1}-{end_date_mmdd}")
    cutoff2 = pd.to_datetime(f"{year2}-{end_date_mmdd}")

    df1 = df[(df["stolen_year"] == year1) & (df["stolen_date"] <= cutoff1)]
    df2 = df[(df["stolen_year"] == year2) & (df["stolen_date"] <= cutoff2)]

    c1 = df1.groupby(dimension).size().reset_index(name=f"stolen_{year1}")
    c2 = df2.groupby(dimension).size().reset_index(name=f"stolen_{year2}")

    out = base.merge(c1, on=dimension, how="left").merge(c2, on=dimension, how="left")
    out[[f"stolen_{year1}", f"stolen_{year2}"]] = out[[f"stolen_{year1}", f"stolen_{year2}"]].fillna(0).astype(int)

    # Growth (avoid divide by zero)
    denom = out[f"stolen_{year1}"].replace(0, np.nan)
    out["growth_pct"] = ((out[f"stolen_{year2}"] - out[f"stolen_{year1}"]) / denom) * 100

    # For plotting focus
    out["is_growth_reliable"] = out[f"stolen_{year1}"] >= min_count_growth

    return out.sort_values("stolen_total", ascending=False)
