"""Tests de l'API FastAPI."""

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from churn.ingest import load_raw_csv  # noqa: E402
from churn.train import train_classifier  # noqa: E402


@pytest.fixture(scope="module")
def api_client():
    """Client API avec modèle entraîné."""
    train_classifier(load_raw_csv())
    from app.api.main import app

    return TestClient(app)


def test_health_endpoint(api_client) -> None:
    response = api_client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ready_endpoint(api_client) -> None:
    response = api_client.get("/ready")
    assert response.status_code == 200


def test_predict_endpoint(api_client) -> None:
    df = load_raw_csv()
    sample = df.drop(columns=["Unnamed: 0", "Attrition_Flag", "CLIENTNUM"], errors="ignore").iloc[0]
    response = api_client.post("/predict", json=sample.to_dict())
    assert response.status_code == 200
    body = response.json()
    assert "probability" in body
    assert body["risk_level"] in {"low", "medium", "high"}


def test_metrics_endpoint(api_client) -> None:
    response = api_client.get("/metrics")
    assert response.status_code == 200
    assert "best_model" in response.json()
