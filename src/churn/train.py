"""Entraînement du modèle de classification churn."""

import json
import logging
from typing import Any

import joblib
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    f1_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import cross_val_score

from churn.config import (
    CLASSIFIER_MODEL_PATH,
    ENCODERS_PATH,
    FEATURE_COLUMNS_PATH,
    METRICS_PATH,
    MODELS_DIR,
    RANDOM_STATE,
)
from churn.features import prepare_train_test_split

logger = logging.getLogger(__name__)


def _evaluate_model(model: Any, x_test: pd.DataFrame, y_test: pd.Series) -> dict[str, float]:
    """Calcule recall, F1 et ROC-AUC sur le jeu de test."""
    y_pred = model.predict(x_test)
    y_proba = model.predict_proba(x_test)[:, 1]
    return {
        "recall": float(recall_score(y_test, y_pred)),
        "f1": float(f1_score(y_test, y_pred)),
        "roc_auc": float(roc_auc_score(y_test, y_proba)),
    }


def train_classifier(df: pd.DataFrame) -> dict[str, Any]:
    """
    Entraîne LR et RF avec SMOTE, sauvegarde le meilleur modèle (recall).

    Returns:
        Dictionnaire des métriques et nom du modèle retenu.
    """
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    x_train, x_test, y_train, y_test, encoders = prepare_train_test_split(df)

    smote = SMOTE(random_state=RANDOM_STATE)
    x_resampled, y_resampled = smote.fit_resample(x_train, y_train)

    candidates = {
        "logistic_regression": LogisticRegression(max_iter=1000, random_state=RANDOM_STATE),
        "random_forest": RandomForestClassifier(
            n_estimators=200,
            random_state=RANDOM_STATE,
            class_weight="balanced",
        ),
    }

    results: dict[str, Any] = {"models": {}}
    best_name = ""
    best_model = None
    best_recall = -1.0

    for name, model in candidates.items():
        model.fit(x_resampled, y_resampled)
        metrics = _evaluate_model(model, x_test, y_test)
        cv_recall = cross_val_score(
            model, x_resampled, y_resampled, cv=3, scoring="recall"
        ).mean()
        metrics["cv_recall"] = float(cv_recall)
        results["models"][name] = metrics
        logger.info("Modèle %s — recall=%.3f", name, metrics["recall"])

        if metrics["recall"] > best_recall:
            best_recall = metrics["recall"]
            best_name = name
            best_model = model

    assert best_model is not None
    results["best_model"] = best_name
    results["classification_report"] = classification_report(y_test, best_model.predict(x_test))

    joblib.dump(best_model, CLASSIFIER_MODEL_PATH)
    joblib.dump(encoders, ENCODERS_PATH)
    FEATURE_COLUMNS_PATH.write_text(json.dumps(list(x_train.columns), indent=2), encoding="utf-8")
    METRICS_PATH.write_text(json.dumps(results, indent=2), encoding="utf-8")

    logger.info("Meilleur modèle : %s (recall=%.3f)", best_name, best_recall)
    return results
