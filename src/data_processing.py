from __future__ import annotations

import pandas as pd


def preprocess_motorbike_thefts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and feature-engineer the dataset.
    - Parses dates
    - Creates year/month/weekday features
    - Creates 'years_to_stole' and 'brand_model'
    """
    df = df.copy()

    # Dates
    df["registration_date"] = pd.to_datetime(df["registration_date"], errors="coerce")
    df["stolen_date"] = pd.to_datetime(df["stolen_date"], errors="coerce")

    # Drop rows without stolen_date (core)
    df = df.dropna(subset=["stolen_date"])

    # Features
    df["stolen_year"] = df["stolen_date"].dt.year
    df["stolen_month"] = df["stolen_date"].dt.month
    df["stolen_weekday"] = df["stolen_date"].dt.weekday
    df["stolen_weekday_name"] = df["stolen_date"].dt.day_name()

    # Antiquity (if registration_date exists)
    df["years_to_stole"] = (df["stolen_date"] - df["registration_date"]).dt.days / 365.25

    # Brand/model convenience
    df["brand_model"] = df["brand"].astype(str) + " - " + df["model"].astype(str)

    return df
