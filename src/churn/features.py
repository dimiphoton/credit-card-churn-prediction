"""Feature engineering et encodage pour le modèle."""

import logging
from typing import Any

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from churn.cleaning import clean_data, split_features_target
from churn.config import RANDOM_STATE, TEST_SIZE

logger = logging.getLogger(__name__)


def encode_categorical_features(
    x: pd.DataFrame,
    encoders: dict[str, LabelEncoder] | None = None,
    fit: bool = True,
) -> tuple[pd.DataFrame, dict[str, LabelEncoder]]:
    """
    Encode les colonnes catégorielles avec LabelEncoder.

    Args:
        x: Features (dont catégorielles).
        encoders: Encodeurs existants (mode inference).
        fit: True = entraîner les encodeurs, False = appliquer existants.

    Returns:
        DataFrame encodé + dictionnaire d'encodeurs.
    """
    encoded = x.copy()
    encoders = encoders or {}

    for column in x.select_dtypes(include=["object", "string"]).columns:
        if fit:
            encoder = LabelEncoder()
            encoded[column] = encoder.fit_transform(encoded[column].astype(str))
            encoders[column] = encoder
        else:
            encoder = encoders[column]
            encoded[column] = encoder.transform(encoded[column].astype(str))

    return encoded, encoders


def prepare_train_test_split(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, dict[str, LabelEncoder]]:
    """
    Pipeline complet : clean → encode → split stratifié.

    Returns:
        X_train, X_test, y_train, y_test, encoders
    """
    x, y = split_features_target(df)
    x_encoded, encoders = encode_categorical_features(x, fit=True)

    x_train, x_test, y_train, y_test = train_test_split(
        x_encoded,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )
    logger.info("Split train/test : %s / %s", len(x_train), len(x_test))
    return x_train, x_test, y_train, y_test, encoders


def transform_single_customer(
    customer: dict[str, Any],
    encoders: dict[str, LabelEncoder],
    feature_columns: list[str],
) -> pd.DataFrame:
    """Transforme un client (dict) en ligne de features pour prédiction."""
    row = pd.DataFrame([customer])
    encoded, _ = encode_categorical_features(row, encoders=encoders, fit=False)
    return encoded[feature_columns]
