"""Tests d'ingestion CSV → SQLite."""

from pathlib import Path

import pytest

from churn.config import CUSTOMERS_TABLE, RAW_DATA_PATH
from churn.ingest import get_customer_count, ingest_csv_to_db, read_customers_from_db


@pytest.fixture
def temp_db(tmp_path: Path) -> Path:
    """Base SQLite temporaire pour les tests."""
    return tmp_path / "test_churn.db"


def test_ingest_csv_to_db(temp_db: Path) -> None:
    row_count = ingest_csv_to_db(db_path=temp_db)
    assert row_count > 0
    assert temp_db.exists()


def test_read_customers_from_db(temp_db: Path) -> None:
    ingest_csv_to_db(db_path=temp_db)
    df = read_customers_from_db(db_path=temp_db)
    assert len(df) > 0
    assert CUSTOMERS_TABLE  # table name constant used
    assert "Attrition_Flag" in df.columns


def test_get_customer_count_matches_csv(temp_db: Path) -> None:
    ingest_csv_to_db(db_path=temp_db)
    db_count = get_customer_count(db_path=temp_db)
    import pandas as pd

    csv_count = len(pd.read_csv(RAW_DATA_PATH))
    assert db_count == csv_count
