"""Shared configuration for the e-commerce data pipeline."""

from pathlib import Path


PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
RAW_DATA_DIR: Path = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR: Path = PROJECT_ROOT / "data" / "processed"

CUSTOMERS_FILE: Path = RAW_DATA_DIR / "customers.csv"
PRODUCTS_FILE: Path = RAW_DATA_DIR / "products.csv"
ORDERS_FILE: Path = RAW_DATA_DIR / "orders.csv"


def ensure_data_directories() -> None:
    """Create the raw and processed data directories if they do not exist."""
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)