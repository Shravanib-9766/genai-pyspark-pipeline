"""Analyze generated e-commerce data with PySpark."""

import logging
from pathlib import Path

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from src.config import CUSTOMERS_FILE, ORDERS_FILE, PRODUCTS_FILE, PROCESSED_DATA_DIR


LOGGER: logging.Logger = logging.getLogger(__name__)


def create_spark_session() -> SparkSession:
    """Create a local Spark session for analytics."""
    return SparkSession.builder.appName("EcommerceAnalytics").master("local[*]").getOrCreate()


def load_data(spark: SparkSession) -> tuple[DataFrame, DataFrame, DataFrame]:
    """Load customers, products, and orders from their raw CSV files."""
    customers: DataFrame = spark.read.option("header", True).option("inferSchema", True).csv(str(CUSTOMERS_FILE))
    products: DataFrame = spark.read.option("header", True).option("inferSchema", True).csv(str(PRODUCTS_FILE))
    orders: DataFrame = spark.read.option("header", True).option("inferSchema", True).csv(str(ORDERS_FILE))
    return customers, products, orders


def build_insights(customers: DataFrame, products: DataFrame, orders: DataFrame) -> dict[str, DataFrame]:
    """Build business insight tables from the three source DataFrames."""
    order_details: DataFrame = orders.join(products, "product_id").withColumn(
        "revenue", F.col("quantity") * F.col("unit_price")
    )
    category_revenue: DataFrame = order_details.groupBy("category").agg(
        F.round(F.sum("revenue"), 2).alias("total_revenue"),
        F.sum("quantity").alias("units_sold"),
    ).orderBy(F.desc("total_revenue"))
    customer_spend: DataFrame = order_details.join(customers, "customer_id").groupBy(
        "customer_id", "name", "email"
    ).agg(F.round(F.sum("revenue"), 2).alias("total_spend")).orderBy(F.desc("total_spend"))
    daily_sales: DataFrame = order_details.groupBy("order_date").agg(
        F.countDistinct("order_id").alias("orders"),
        F.round(F.sum("revenue"), 2).alias("daily_revenue"),
    ).orderBy("order_date")
    top_products: DataFrame = order_details.groupBy("product_id", "product_name", "category").agg(
        F.round(F.sum("revenue"), 2).alias("total_revenue"),
        F.sum("quantity").alias("units_sold"),
    ).orderBy(F.desc("total_revenue")).limit(10)
    return {
        "category_revenue": category_revenue,
        "customer_spend": customer_spend,
        "daily_sales": daily_sales,
        "top_products": top_products,
    }


def write_insights(insights: dict[str, DataFrame], output_dir: Path = PROCESSED_DATA_DIR) -> None:
    """Write each insight table as an overwrite-mode CSV directory."""
    for name, data in insights.items():
        output_path: Path = output_dir / name
        data.coalesce(1).write.mode("overwrite").option("header", True).csv(str(output_path))
        LOGGER.info("Wrote insight table to %s", output_path)


def run_analytics() -> None:
    """Load raw data, calculate insights, and persist processed results."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    spark: SparkSession = create_spark_session()
    try:
        customers, products, orders = load_data(spark)
        write_insights(build_insights(customers, products, orders))
    finally:
        spark.stop()


if __name__ == "__main__":
    run_analytics()