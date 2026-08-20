# E-commerce PySpark Pipeline

Generate realistic synthetic e-commerce data and analyze it with PySpark.
The project creates customer, product, and order CSV files in `data/raw/`, then
writes business insight tables to `data/processed/`.

## Project Structure

```text
.
|-- data/
|   |-- processed/
|   `-- raw/
|-- notebooks/
|   `-- ecommerce_analysis.ipynb
|-- src/
|   |-- __init__.py
|   |-- config.py
|   |-- data_generator.py
|   `-- spark_analytics.py
|-- tests/
|   `-- test_data_generator.py
|-- .gitignore
|-- README.md
`-- requirements.txt
```

## Setup

Use Python 3.10 or newer and Java 8, 11, or 17 for PySpark.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run the Pipeline

Generate 1,000 customers, 100 products, and 5,000 orders:

```powershell
python -m src.data_generator
python -m src.spark_analytics
```

Override the generated row counts when needed:

```powershell
python -m src.data_generator --customers 500 --products 50 --orders 2000 --seed 42
```

The analytics job produces these CSV-backed result directories:

- `data/processed/category_revenue/`
- `data/processed/customer_spend/`
- `data/processed/daily_sales/`
- `data/processed/top_products/`

Run the tests with:

```powershell
pytest
```
