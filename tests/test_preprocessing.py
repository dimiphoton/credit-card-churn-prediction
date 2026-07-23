"""Tests de nettoyage et feature engineering."""

import pandas as pd

from churn.cleaning import clean_data, split_features_target
from churn.config import CLIENT_ID_COLUMN, DROP_COLUMNS, TARGET_COLUMN
from churn.features import encode_categorical_features, prepare_train_test_split
from churn.ingest import load_raw_csv


def test_clean_data_removes_index_column() -> None:
    df = load_raw_csv()
    cleaned = clean_data(df)
    for col in DROP_COLUMNS:
        assert col not in cleaned.columns


def test_clean_data_no_duplicates_on_client_id() -> None:
    df = load_raw_csv()
    cleaned = clean_data(df)
    assert cleaned[CLIENT_ID_COLUMN].is_unique


def test_split_features_target_binary() -> None:
    df = load_raw_csv()
    x, y = split_features_target(df)
    assert TARGET_COLUMN not in x.columns
    assert CLIENT_ID_COLUMN not in x.columns
    assert set(y.unique()).issubset({0, 1})


def test_encode_categorical_produces_numeric() -> None:
    df = load_raw_csv()
    x, _ = split_features_target(df)
    encoded, encoders = encode_categorical_features(x, fit=True)
    assert len(encoders) >= 1
    assert encoded.select_dtypes(include=["object"]).shape[1] == 0


def test_prepare_train_test_split_shapes() -> None:
    df = load_raw_csv()
    x_train, x_test, y_train, y_test, encoders = prepare_train_test_split(df)
    assert len(x_train) > len(x_test)
    assert len(x_train) == len(y_train)
    assert len(x_test) == len(y_test)
    assert len(encoders) >= 1
