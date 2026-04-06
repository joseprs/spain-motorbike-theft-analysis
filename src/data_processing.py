from __future__ import annotations

import pandas as pd
import unicodedata
import re


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

    print(f"Stolen motorbikes from {min(df.stolen_date)} to {max(df.stolen_date)}.")

    return df


def normalize_province_name(x):
    if pd.isna(x):
        return None

    x = re.sub(r"^\d+\s+", "", x)
    x = x.split("/")[0]
    x = x.lower()
    x = unicodedata.normalize("NFKD", x)
    x = "".join(c for c in x if not unicodedata.combining(c))

    x = x.replace(",", "")
    x = re.sub(r"\b(la|las|el|els|a)\b\s*", "", x)
    x = x.strip()

    return x


def transform_province_names(df, column):
    province_to_code = {"albacete": "AB","alicante": "A","almeria": "AL","araba": "VI","avila": "AV",
                    "badajoz": "BA","balears illes": "IB","barcelona": "B","bizkaia": "BI","burgos": "BU",
                    "caceres": "CC","cadiz": "CA","cantabria": "S","castellon": "CS","ciudad real": "CR",
                    "cordoba": "CO","coruna": "C","cuenca": "CU","gipuzkoa": "SS","girona": "GI",
                    "granada": "GR","guadalajara": "GU","huelva": "H","huesca": "HU","jaen": "J",
                    "leon": "LE","lleida": "L","lugo": "LU","madrid": "M","malaga": "MA","murcia": "MU",
                    "navarra": "NA","ourense": "OU","palencia": "P","palmas": "GC","pontevedra": "PO",
                    "rioja": "LO","salamanca": "SA","santa cruz de tenerife": "TF","segovia": "SG",
                    "sevilla": "SE","soria": "SO","tarragona": "T","teruel": "TE",
                    "toledo": "TO","valencia": "V","valladolid": "VA","zamora": "ZA","zaragoza": "Z",
                    "ceuta": "CE","melilla": "ML",
    }
    df = df.copy()
    df[column] = df[column].apply(normalize_province_name)
    df["province_code"] = df[column].map(province_to_code)
    df = df[df["Provincias"] != "total espana"].reset_index(drop=True)
    return df
