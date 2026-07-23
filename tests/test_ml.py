"""Tests des modèles ML (classification + clustering)."""

import json

import joblib
import pytest

from churn.config import (
    CLASSIFIER_MODEL_PATH,
    CLUSTERING_MODEL_PATH,
    ENCODERS_PATH,
    FEATURE_COLUMNS_PATH,
    METRICS_PATH,
    CLUSTER_PROFILES_PATH,
)
from churn.ingest import load_raw_csv
from churn.predict import load_classifier_artifacts, predict_churn
from churn.clustering import train_clustering
from churn.train import train_classifier


@pytest.fixture(scope="module")
def trained_artifacts():
    """Entraîne les modèles une fois pour tous les tests du module."""
    df = load_raw_csv()
    metrics = train_classifier(df)
    clusters = train_clustering(df)
    return metrics, clusters


def test_train_classifier_creates_model_files(trained_artifacts) -> None:
    assert CLASSIFIER_MODEL_PATH.exists()
    assert ENCODERS_PATH.exists()
    assert FEATURE_COLUMNS_PATH.exists()
    assert METRICS_PATH.exists()


def test_best_model_metrics(trained_artifacts) -> None:
    metrics, _ = trained_artifacts
    assert "best_model" in metrics
    assert metrics["models"][metrics["best_model"]]["recall"] > 0


def test_train_clustering_creates_files(trained_artifacts) -> None:
    assert CLUSTERING_MODEL_PATH.exists()
    assert CLUSTER_PROFILES_PATH.exists()
    profiles = json.loads(CLUSTER_PROFILES_PATH.read_text(encoding="utf-8"))
    assert profiles["best_k"] >= 2


def test_predict_churn_sample(trained_artifacts) -> None:
    df = load_raw_csv()
    sample = df.drop(columns=["Unnamed: 0", "Attrition_Flag"], errors="ignore").iloc[0].to_dict()
    result = predict_churn(sample)
    assert "probability" in result
    assert result["risk_level"] in {"low", "medium", "high"}


def test_load_classifier_artifacts(trained_artifacts) -> None:
    model, encoders, columns = load_classifier_artifacts()
    assert model is not None
    assert len(encoders) >= 1
    assert len(columns) >= 1
