"""Clustering KMeans — segmentation clients."""

import json
import logging
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

from churn.cleaning import clean_data, split_features_target
from churn.config import (
    CLUSTER_PROFILES_PATH,
    CLUSTERING_MODEL_PATH,
    MODELS_DIR,
    RANDOM_STATE,
    SCALER_PATH,
    TARGET_COLUMN,
)
from churn.features import encode_categorical_features

logger = logging.getLogger(__name__)

K_RANGE = range(2, 9)


def find_optimal_k(x_scaled: np.ndarray) -> dict[str, Any]:
    """Trouve K optimal via score de silhouette."""
    scores: dict[int, float] = {}
    for k in K_RANGE:
        model = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=10)
        labels = model.fit_predict(x_scaled)
        scores[k] = float(silhouette_score(x_scaled, labels))

    best_k = max(scores, key=scores.get)
    logger.info("K optimal = %s (silhouette=%.3f)", best_k, scores[best_k])
    return {"best_k": best_k, "silhouette_scores": scores}


def build_cluster_profiles(df: pd.DataFrame, labels: np.ndarray) -> list[dict[str, Any]]:
    """Décrit chaque cluster (taille, churn rate, profil numérique moyen)."""
    from churn.config import CHURN_POSITIVE_LABEL

    profile_df = df.copy()
    profile_df["cluster"] = labels
    profiles: list[dict[str, Any]] = []

    numeric_cols = profile_df.select_dtypes(include=["number"]).columns.tolist()
    numeric_cols = [c for c in numeric_cols if c not in ("cluster",)]

    for cluster_id in sorted(profile_df["cluster"].unique()):
        subset = profile_df[profile_df["cluster"] == cluster_id]
        churn_rate = (subset[TARGET_COLUMN] == CHURN_POSITIVE_LABEL).mean()
        profiles.append(
            {
                "cluster_id": int(cluster_id),
                "size": int(len(subset)),
                "churn_rate": float(churn_rate),
                "avg_customer_age": float(subset["Customer_Age"].mean()),
                "avg_credit_limit": float(subset["Credit_Limit"].mean()),
                "avg_total_trans_amt": float(subset["Total_Trans_Amt"].mean()),
            }
        )
    return profiles


def train_clustering(df: pd.DataFrame) -> dict[str, Any]:
    """
    Entraîne KMeans sur features normalisées et sauvegarde modèle + profils.

    Returns:
        Métadonnées clustering (K, scores, profils).
    """
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    cleaned = clean_data(df)
    x, _ = split_features_target(cleaned)
    x_encoded, _ = encode_categorical_features(x, fit=True)

    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x_encoded)

    k_info = find_optimal_k(x_scaled)
    best_k = k_info["best_k"]

    kmeans = KMeans(n_clusters=best_k, random_state=RANDOM_STATE, n_init=10)
    labels = kmeans.fit_predict(x_scaled)

    profiles = build_cluster_profiles(cleaned, labels)
    result = {**k_info, "cluster_profiles": profiles}

    joblib.dump(kmeans, CLUSTERING_MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    CLUSTER_PROFILES_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")

    logger.info("Clustering terminé — %s clusters", best_k)
    return result
