"""API FastAPI — prédiction de churn (stub, branch 01)."""

from fastapi import FastAPI

app = FastAPI(
    title="Churn Prediction API",
    description="API de prédiction du taux de churn client.",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    """Vérifie que l'API répond."""
    return {"status": "ok"}
