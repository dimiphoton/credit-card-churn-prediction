"""Ingestion CSV vers SQLite."""

import logging
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from churn.config import CUSTOMERS_TABLE, DB_PATH, PROCESSED_DATA_DIR, RAW_DATA_PATH

logger = logging.getLogger(__name__)


def _build_engine(db_path: Path) -> Engine:
    """Crée un moteur SQLAlchemy pour SQLite."""
    return create_engine(f"sqlite:///{db_path}")


def load_raw_csv(csv_path: Path | None = None) -> pd.DataFrame:
    """Charge le CSV brut en DataFrame pandas."""
    path = csv_path or RAW_DATA_PATH
    logger.info("Chargement du CSV : %s", path)
    return pd.read_csv(path)


def ingest_csv_to_db(
    csv_path: Path | None = None,
    db_path: Path | None = None,
    if_exists: str = "replace",
) -> int:
    """
    Importe le CSV dans SQLite.

    Returns:
        Nombre de lignes insérées.
    """
    csv_path = csv_path or RAW_DATA_PATH
    db_path = db_path or DB_PATH
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    df = load_raw_csv(csv_path)
    engine = _build_engine(db_path)
    df.to_sql(CUSTOMERS_TABLE, engine, if_exists=if_exists, index=False)
    row_count = len(df)
    logger.info("%s lignes importées dans %s", row_count, db_path)
    return row_count


def read_customers_from_db(db_path: Path | None = None) -> pd.DataFrame:
    """Lit la table clients depuis SQLite."""
    db_path = db_path or DB_PATH
    engine = _build_engine(db_path)
    query = text(f"SELECT * FROM {CUSTOMERS_TABLE}")
    with engine.connect() as connection:
        return pd.read_sql(query, connection)


def get_customer_count(db_path: Path | None = None) -> int:
    """Retourne le nombre de clients en base."""
    db_path = db_path or DB_PATH
    engine = _build_engine(db_path)
    query = text(f"SELECT COUNT(*) AS n FROM {CUSTOMERS_TABLE}")
    with engine.connect() as connection:
        result = connection.execute(query).scalar_one()
    return int(result)
