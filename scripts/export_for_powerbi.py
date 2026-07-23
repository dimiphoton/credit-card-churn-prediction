"""Exporte un CSV enrichi ML pour Power BI et Tableau."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from churn.cleaning import clean_data
from churn.config import CHURN_POSITIVE_LABEL
from churn.ingest import load_raw_csv
from churn.predict import add_ml_predictions

POWERBI_PATH = PROJECT_ROOT / "powerbi" / "data" / "bank_churn_powerbi.csv"
TABLEAU_PATH = PROJECT_ROOT / "tableau" / "data" / "bank_churn_tableau.csv"


def build_bi_dataset():
    """Construit le dataset BI avec labels + prédictions ML."""
    df = clean_data(load_raw_csv())
    df = add_ml_predictions(df)

    df["IsChurn"] = (df["Attrition_Flag"] == CHURN_POSITIVE_LABEL).astype(int)
    df["ChurnLabel"] = df["Attrition_Flag"].map(
        {
            CHURN_POSITIVE_LABEL: "Churned",
            "Existing Customer": "Active",
        }
    )
    return df


def export_for_bi() -> None:
    """Exporte le même fichier ML-enriched vers Power BI et Tableau."""
    df = build_bi_dataset()

    for path in (POWERBI_PATH, TABLEAU_PATH):
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(path, index=False)
        print(f"Export BI : {path} ({len(df)} rows, {len(df.columns)} cols)")


if __name__ == "__main__":
    export_for_bi()
