"""Inférence — prédiction churn."""

import json
import logging
from typing import Any

import joblib
import numpy as np
import pandas as pd

from churn.config import (
    CLASSIFIER_MODEL_PATH,
    CLUSTERING_MODEL_PATH,
    ENCODERS_PATH,
    FEATURE_COLUMNS_PATH,
    SCALER_PATH,
)
from churn.features import encode_categorical_features, transform_single_customer
from churn.cleaning import split_features_target

logger = logging.getLogger(__name__)


def load_classifier_artifacts() -> tuple[Any, dict, list[str]]:
    """Charge modèle, encodeurs et liste de colonnes features."""
    model = joblib.load(CLASSIFIER_MODEL_PATH)
    encoders = joblib.load(ENCODERS_PATH)
    feature_columns = json.loads(FEATURE_COLUMNS_PATH.read_text(encoding="utf-8"))
    return model, encoders, feature_columns


def _risk_level_from_probability(probability: float) -> str:
    """Convertit une probabilité en niveau de risque."""
    if probability >= 0.7:
        return "high"
    if probability >= 0.4:
        return "medium"
    return "low"


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
    risk_level = _risk_level_from_probability(probability)

    return {
        "churn": churn,
        "probability": round(probability, 4),
        "risk_level": risk_level,
    }


def add_ml_predictions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enrichit un DataFrame nettoyé avec scores ML (classification + clustering).

    Colonnes ajoutées :
        ChurnProbability, PredictedChurn, RiskLevel, ML_Cluster, PredictionMatch
    """
    enriched = df.copy()

    if not CLASSIFIER_MODEL_PATH.exists():
        logger.warning("Modèle absent — lancer scripts/run_training.py avant l'export BI")
        return enriched

    x, y_actual = split_features_target(df)
    model, encoders, feature_columns = load_classifier_artifacts()
    x_encoded, _ = encode_categorical_features(x, encoders=encoders, fit=False)
    x_encoded = x_encoded[feature_columns]

    probabilities = model.predict_proba(x_encoded)[:, 1]
    predictions = model.predict(x_encoded)

    enriched["ChurnProbability"] = probabilities.round(4)
    enriched["PredictedChurn"] = predictions.astype(int)
    enriched["RiskLevel"] = [_risk_level_from_probability(float(p)) for p in probabilities]
    matches = predictions == y_actual.values
    enriched["PredictionMatch"] = np.where(matches, "Correct", "Incorrect")

    if CLUSTERING_MODEL_PATH.exists() and SCALER_PATH.exists():
        kmeans = joblib.load(CLUSTERING_MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        x_scaled = scaler.transform(x_encoded)
        enriched["ML_Cluster"] = kmeans.predict(x_scaled).astype(int)

    logger.info("Prédictions ML ajoutées pour %s clients", len(enriched))
    return enriched


def load_metrics() -> dict[str, Any]:
    """Charge les métriques sauvegardées à l'entraînement."""
    from churn.config import METRICS_PATH

    return json.loads(METRICS_PATH.read_text(encoding="utf-8"))


def load_cluster_profiles() -> dict[str, Any]:
    """Charge les profils de clusters."""
    from churn.config import CLUSTER_PROFILES_PATH

    return json.loads(CLUSTER_PROFILES_PATH.read_text(encoding="utf-8"))
