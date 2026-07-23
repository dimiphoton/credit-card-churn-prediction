"""Inférence — prédiction churn."""

import json
import logging
from typing import Any

import joblib
import pandas as pd

from churn.config import (
    CLASSIFIER_MODEL_PATH,
    ENCODERS_PATH,
    FEATURE_COLUMNS_PATH,
)
from churn.features import transform_single_customer

logger = logging.getLogger(__name__)


def load_classifier_artifacts() -> tuple[Any, dict, list[str]]:
    """Charge modèle, encodeurs et liste de colonnes features."""
    model = joblib.load(CLASSIFIER_MODEL_PATH)
    encoders = joblib.load(ENCODERS_PATH)
    feature_columns = json.loads(FEATURE_COLUMNS_PATH.read_text(encoding="utf-8"))
    return model, encoders, feature_columns


def predict_churn(customer: dict[str, Any]) -> dict[str, Any]:
    """
    Prédit la probabilité de churn pour un client.

    Returns:
        dict avec churn (bool), probability (float), risk_level (str)
    """
    model, encoders, feature_columns = load_classifier_artifacts()
    features = transform_single_customer(customer, encoders, feature_columns)

    probability = float(model.predict_proba(features)[0, 1])
    churn = probability >= 0.5

    if probability >= 0.7:
        risk_level = "high"
    elif probability >= 0.4:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {
        "churn": churn,
        "probability": round(probability, 4),
        "risk_level": risk_level,
    }


def load_metrics() -> dict[str, Any]:
    """Charge les métriques sauvegardées à l'entraînement."""
    from churn.config import METRICS_PATH

    return json.loads(METRICS_PATH.read_text(encoding="utf-8"))


def load_cluster_profiles() -> dict[str, Any]:
    """Charge les profils de clusters."""
    from churn.config import CLUSTER_PROFILES_PATH

    return json.loads(CLUSTER_PROFILES_PATH.read_text(encoding="utf-8"))
