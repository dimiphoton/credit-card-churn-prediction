"""API FastAPI — prédiction de churn."""

import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Permet d'importer le package churn depuis src/
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from churn.config import CLASSIFIER_MODEL_PATH, METRICS_PATH  # noqa: E402
from churn.predict import load_metrics, predict_churn  # noqa: E402

app = FastAPI(
    title="Churn Prediction API",
    description="API de prédiction du taux de churn client pour l'équipe marketing.",
    version="1.0.0",
)


class CustomerInput(BaseModel):
    """Features client pour la prédiction (sans CLIENTNUM ni Attrition_Flag)."""

    Customer_Age: int = Field(..., ge=18, le=100)
    Gender: str
    Dependent_count: int = Field(..., ge=0)
    Education_Level: str
    Marital_Status: str
    Income_Category: str
    Card_Category: str
    Months_on_book: int = Field(..., ge=0)
    Total_Relationship_Count: int = Field(..., ge=1)
    Months_Inactive_12_mon: int = Field(..., ge=0)
    Contacts_Count_12_mon: int = Field(..., ge=0)
    Credit_Limit: float = Field(..., ge=0)
    Total_Revolving_Bal: float = Field(..., ge=0)
    Avg_Open_To_Buy: float = Field(..., ge=0)
    Total_Amt_Chng_Q4_Q1: float = Field(..., ge=0)
    Total_Trans_Amt: float = Field(..., ge=0)
    Total_Trans_Ct: int = Field(..., ge=0)
    Total_Ct_Chng_Q4_Q1: float = Field(..., ge=0)
    Avg_Utilization_Ratio: float = Field(..., ge=0, le=1)


class PredictionResponse(BaseModel):
    churn: bool
    probability: float
    risk_level: str


@app.get("/health")
def health() -> dict[str, str]:
    """Vérifie que l'API répond."""
    return {"status": "ok"}


@app.get("/ready")
def ready() -> dict[str, str]:
    """Vérifie que le modèle est disponible."""
    if not CLASSIFIER_MODEL_PATH.exists():
        raise HTTPException(status_code=503, detail="Modèle non entraîné")
    return {"status": "ready"}


@app.post("/predict", response_model=PredictionResponse)
def predict(customer: CustomerInput) -> PredictionResponse:
    """Prédit la probabilité de churn pour un client."""
    if not CLASSIFIER_MODEL_PATH.exists():
        raise HTTPException(
            status_code=503,
            detail="Modèle absent. Exécuter scripts/run_training.py",
        )
    result = predict_churn(customer.model_dump())
    return PredictionResponse(**result)


@app.get("/metrics")
def metrics() -> dict:
    """Retourne les métriques du modèle entraîné."""
    if not METRICS_PATH.exists():
        raise HTTPException(status_code=503, detail="Métriques absentes")
    return load_metrics()
