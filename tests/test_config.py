"""Tests de configuration et chemins du projet."""

from churn.config import (
    CATEGORICAL_COLUMNS,
    PROJECT_ROOT,
    RAW_DATA_PATH,
    TARGET_COLUMN,
)


def test_project_root_exists() -> None:
    assert PROJECT_ROOT.is_dir()


def test_raw_data_file_exists() -> None:
    assert RAW_DATA_PATH.exists(), f"Dataset introuvable : {RAW_DATA_PATH}"


def test_target_column_defined() -> None:
    assert TARGET_COLUMN == "Attrition_Flag"


def test_categorical_columns_not_empty() -> None:
    assert len(CATEGORICAL_COLUMNS) >= 1
