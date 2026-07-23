"""Tests d'intégration — pipeline complet."""

from pathlib import Path

import pytest

from churn.ingest import get_customer_count, ingest_csv_to_db, read_customers_from_db
from churn.predict import load_metrics, predict_churn
from churn.train import train_classifier
from churn.clustering import train_clustering


@pytest.fixture(scope="module")
def pipeline_db(tmp_path_factory) -> Path:
    """Base temporaire + entraînement complet."""
    db_path = tmp_path_factory.mktemp("pipeline") / "pipeline.db"
    ingest_csv_to_db(db_path=db_path)
    df = read_customers_from_db(db_path=db_path)
    train_classifier(df)
    train_clustering(df)
    return db_path


def test_pipeline_db_row_count(pipeline_db: Path) -> None:
    assert get_customer_count(db_path=pipeline_db) == 10127


def test_pipeline_metrics_available(pipeline_db: Path) -> None:
    metrics = load_metrics()
    assert metrics["best_model"] in {"logistic_regression", "random_forest"}


def test_pipeline_predict_after_training(pipeline_db: Path) -> None:
    df = read_customers_from_db(db_path=pipeline_db)
    customer = df.drop(columns=["Unnamed: 0", "Attrition_Flag"], errors="ignore").iloc[5].to_dict()
    result = predict_churn(customer)
    assert 0.0 <= result["probability"] <= 1.0
