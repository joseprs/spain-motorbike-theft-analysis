from __future__ import annotations

from io import StringIO
from pathlib import Path
import pandas as pd


def load_raw_dgt_csv(path: str | Path) -> pd.DataFrame:
    """
    Load the raw DGT CSV that may contain conflicting quotes.
    We read as text, sanitize, then parse with pandas.
    Returns a DataFrame with raw columns (no typing assumptions yet).
    """
    path = Path(path)
    text = path.read_text(encoding="utf-8", errors="replace")
    cleaned = text.replace('""', "").replace('"', "").strip()

    df = pd.read_csv(StringIO(cleaned), delimiter=",")
    return df


def load_province_population(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    text = path.read_text(encoding="latin-1", errors="replace")
    cleaned = text.replace('""', "").replace('"', "").strip()
    return pd.read_csv(StringIO(cleaned), encoding="latin-1", sep=";")
