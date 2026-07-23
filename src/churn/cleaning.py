"""Nettoyage et préparation des données brutes."""

import logging

import pandas as pd

from churn.config import (
    CATEGORICAL_COLUMNS,
    CLIENT_ID_COLUMN,
    DROP_COLUMNS,
    TARGET_COLUMN,
)

logger = logging.getLogger(__name__)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoie le DataFrame : supprime colonnes inutiles, doublons et nulls.

    Args:
        df: DataFrame brut.

    Returns:
        DataFrame nettoyé.
    """
    cleaned = df.copy()

    cols_to_drop = [col for col in DROP_COLUMNS if col in cleaned.columns]
    if cols_to_drop:
        cleaned = cleaned.drop(columns=cols_to_drop)

    cleaned = cleaned.drop_duplicates(subset=[CLIENT_ID_COLUMN])
    cleaned = cleaned.dropna()

    logger.info("Nettoyage terminé : %s lignes restantes", len(cleaned))
    return cleaned


def split_features_target(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Sépare X (features) et y (cible binaire churn=1)."""
    from churn.config import CHURN_POSITIVE_LABEL

    cleaned = clean_data(df)
    y = (cleaned[TARGET_COLUMN] == CHURN_POSITIVE_LABEL).astype(int)
    feature_cols = [col for col in cleaned.columns if col not in (TARGET_COLUMN, CLIENT_ID_COLUMN)]
    x = cleaned[feature_cols]
    return x, y


def get_categorical_columns(df: pd.DataFrame) -> list[str]:
    """Retourne les colonnes catégorielles présentes dans le DataFrame."""
    return [col for col in CATEGORICAL_COLUMNS if col in df.columns]
