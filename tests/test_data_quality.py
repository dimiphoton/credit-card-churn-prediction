"""Tests unitaires complémentaires."""

import pytest

from churn.cleaning import clean_data
from churn.ingest import load_raw_csv


def test_no_null_values_after_cleaning() -> None:
    df = load_raw_csv()
    cleaned = clean_data(df)
    assert cleaned.isnull().sum().sum() == 0


def test_dataset_minimum_size() -> None:
    df = load_raw_csv()
    assert len(df) >= 10_000


@pytest.mark.parametrize(
    "required_column",
    [
        "CLIENTNUM",
        "Attrition_Flag",
        "Customer_Age",
        "Credit_Limit",
        "Total_Trans_Amt",
    ],
)
def test_required_columns_present(required_column: str) -> None:
    df = load_raw_csv()
    assert required_column in df.columns
