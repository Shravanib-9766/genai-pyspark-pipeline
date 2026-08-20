"""Generate deterministic synthetic e-commerce data as CSV files."""

import argparse
import logging
import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
from faker import Faker

from src.config import CUSTOMERS_FILE, ORDERS_FILE, PRODUCTS_FILE, ensure_data_directories


LOGGER: logging.Logger = logging.getLogger(__name__)


def configure_logging() -> None:
    """Configure application logging for command-line execution."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


def generate_customers(count: int, fake: Faker) -> pd.DataFrame:
    """Return a DataFrame containing synthetic customer records."""
    return pd.DataFrame(
        {
            "customer_id": [f"C{i:05d}" for i in range(1, count + 1)],
            "name": [fake.name() for _ in range(count)],
            "email": [fake.unique.email() for _ in range(count)],
            "city": [fake.city() for _ in range(count)],
            "signup_date": [fake.date_between(start_date="-3y", end_date="today") for _ in range(count)],
        }
    )


def generate_products(count: int, fake: Faker) -> pd.DataFrame:
    """Return a DataFrame containing synthetic product records."""
    categories: list[str] = ["Electronics", "Home", "Books", "Fitness", "Apparel"]
    return pd.DataFrame(
        {
            "product_id": [f"P{i:05d}" for i in range(1, count + 1)],
            "product_name": [fake.catch_phrase() for _ in range(count)],
            "category": [random.choice(categories) for _ in range(count)],
            "unit_price": [round(random.uniform(9.99, 499.99), 2) for _ in range(count)],
        }
    )


def generate_orders(count: int, customer_count: int, product_count: int) -> pd.DataFrame:
    """Return a DataFrame containing synthetic order line records."""
    start_date: date = date.today() - timedelta(days=365)
    return pd.DataFrame(
        {
            "order_id": [f"O{i:06d}" for i in range(1, count + 1)],
            "customer_id": [f"C{random.randint(1, customer_count):05d}" for _ in range(count)],
            "product_id": [f"P{random.randint(1, product_count):05d}" for _ in range(count)],
            "quantity": [random.randint(1, 5) for _ in range(count)],
            "order_date": [start_date + timedelta(days=random.randint(0, 365)) for _ in range(count)],
        }
    )


def write_csv(data: pd.DataFrame, path: Path) -> None:
    """Write a DataFrame to CSV, creating its parent directory first."""
    path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(path, index=False)
    LOGGER.info("Wrote %d rows to %s", len(data), path)


def generate_data(customer_count: int, product_count: int, order_count: int, seed: int = 42) -> None:
    """Generate and persist all synthetic source datasets."""
    if min(customer_count, product_count, order_count) < 1:
        raise ValueError("All record counts must be positive")
    random.seed(seed)
    fake: Faker = Faker()
    fake.seed_instance(seed)
    ensure_data_directories()
    write_csv(generate_customers(customer_count, fake), CUSTOMERS_FILE)
    write_csv(generate_products(product_count, fake), PRODUCTS_FILE)
    write_csv(generate_orders(order_count, customer_count, product_count), ORDERS_FILE)


def parse_args() -> argparse.Namespace:
    """Parse command-line options for the data generator."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--customers", type=int, default=1000)
    parser.add_argument("--products", type=int, default=100)
    parser.add_argument("--orders", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def main() -> None:
    """Run the data generator from the command line."""
    configure_logging()
    args: argparse.Namespace = parse_args()
    generate_data(args.customers, args.products, args.orders, args.seed)


if __name__ == "__main__":
    main()