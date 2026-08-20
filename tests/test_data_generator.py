"""Tests for synthetic source data generation."""

from faker import Faker

from src.data_generator import generate_customers, generate_orders, generate_products


def test_generated_data_has_expected_shapes() -> None:
    """Generated tables contain the requested number of rows and columns."""
    fake: Faker = Faker()
    customers = generate_customers(3, fake)
    products = generate_products(2, fake)
    orders = generate_orders(5, 3, 2)

    assert customers.shape == (3, 5)
    assert products.shape == (2, 4)
    assert orders.shape == (5, 5)
    assert set(orders["customer_id"]).issubset(set(customers["customer_id"]))
    assert set(orders["product_id"]).issubset(set(products["product_id"]))