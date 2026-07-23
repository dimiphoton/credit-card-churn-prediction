"""Script CLI — exécute ingestion + entraînement ML."""

import logging
import sys
from pathlib import Path

# Permet d'importer churn sans PYTHONPATH (Render build, CI, etc.)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from churn.clustering import train_clustering
from churn.ingest import ingest_csv_to_db, read_customers_from_db
from churn.train import train_classifier

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")


def main() -> None:
    """Lance le pipeline complet de modélisation."""
    ingest_csv_to_db()
    df = read_customers_from_db()
    train_classifier(df)
    train_clustering(df)
    print("Pipeline ML terminé.")


if __name__ == "__main__":
    main()
