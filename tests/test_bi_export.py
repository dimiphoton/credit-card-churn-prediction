"""Tests export BI avec colonnes ML."""

import pandas as pd

from churn.cleaning import clean_data
from churn.ingest import load_raw_csv
from churn.predict import add_ml_predictions
from churn.train import train_classifier


def test_add_ml_predictions_columns() -> None:
    df = load_raw_csv()
    train_classifier(df)
    cleaned = clean_data(df)
    enriched = add_ml_predictions(cleaned)

    assert "ChurnProbability" in enriched.columns
    assert "PredictedChurn" in enriched.columns
    assert "RiskLevel" in enriched.columns
    assert "ML_Cluster" in enriched.columns
    assert "PredictionMatch" in enriched.columns
    assert enriched["ChurnProbability"].between(0, 1).all()
