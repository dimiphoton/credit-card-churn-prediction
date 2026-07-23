"""Chemins et constantes partagés par tout le projet."""

from pathlib import Path

# Racine du dépôt (src/churn/config.py → remonte de 2 niveaux)
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Données
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_PATH = DATA_DIR / "raw_data" / "bank_data.csv"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
DB_PATH = PROCESSED_DATA_DIR / "churn.db"

# Artefacts ML
MODELS_DIR = PROJECT_ROOT / "models"
CLASSIFIER_MODEL_PATH = MODELS_DIR / "classifier.pkl"
CLUSTERING_MODEL_PATH = MODELS_DIR / "clustering.pkl"

# Colonnes métier
TARGET_COLUMN = "Attrition_Flag"
CLIENT_ID_COLUMN = "CLIENTNUM"
CATEGORICAL_COLUMNS = [
    "Gender",
    "Education_Level",
    "Marital_Status",
    "Income_Category",
    "Card_Category",
]
DROP_COLUMNS = ["Unnamed: 0"]  # index CSV exporté par pandas

# Valeurs cible
CHURN_POSITIVE_LABEL = "Attrited Customer"
CHURN_NEGATIVE_LABEL = "Existing Customer"

# Reproductibilité
RANDOM_STATE = 42
