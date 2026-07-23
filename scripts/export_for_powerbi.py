"""Exporte un CSV propre pour Power BI Desktop."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import pandas as pd

from churn.cleaning import clean_data
from churn.config import CHURN_POSITIVE_LABEL, RAW_DATA_PATH
from churn.ingest import load_raw_csv

OUTPUT_DIR = PROJECT_ROOT / "powerbi" / "data"
OUTPUT_PATH = OUTPUT_DIR / "bank_churn_powerbi.csv"


def export_for_powerbi() -> Path:
    """Nettoie les données et ajoute des colonnes utiles pour Power BI."""
    df = clean_data(load_raw_csv())

    # Colonnes calculées — plus simples à utiliser dans Power BI / DAX
    df["IsChurn"] = (df["Attrition_Flag"] == CHURN_POSITIVE_LABEL).astype(int)
    df["ChurnLabel"] = df["Attrition_Flag"].map(
        {
            CHURN_POSITIVE_LABEL: "Churned",
            "Existing Customer": "Active",
        }
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Export Power BI : {OUTPUT_PATH} ({len(df)} rows)")
    return OUTPUT_PATH


if __name__ == "__main__":
    export_for_powerbi()
