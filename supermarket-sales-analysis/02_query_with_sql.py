from pathlib import Path
import sqlite3
import pandas as pd

base_dir = Path(__file__).resolve().parent
cleaned_csv = base_dir / "output" / "cleaned_superstore_data.csv"
db_path = base_dir / "output" / "superstore.db"

if not cleaned_csv.exists():
    raise FileNotFoundError(
        f"Cleaned CSV not found at {cleaned_csv}. Run 01_data_cleaning.py first."
    )

print(f"Loading cleaned data from: {cleaned_csv}")
df = pd.read_csv(cleaned_csv, parse_dates=["order_date", "ship_date"])

print(f"Writing data into SQLite database: {db_path}")
with sqlite3.connect(db_path) as conn:
    df.to_sql("superstore", conn, if_exists="replace", index=False)

    example_queries = [
        (
            "Top 10 orders by sales",
            "SELECT order_id, region, category, sales, profit"
            " FROM superstore"
            " ORDER BY sales DESC"
            " LIMIT 10",
        ),
        (
            "Sales and profit by region",
            "SELECT region, COUNT(*) AS orders,"
            " ROUND(SUM(sales), 2) AS total_sales,"
            " ROUND(SUM(profit), 2) AS total_profit"
            " FROM superstore"
            " GROUP BY region"
            " ORDER BY total_sales DESC",
        ),
        (
            "Average profit margin by segment",
            "SELECT segment, ROUND(AVG(profit_margin), 4) AS avg_profit_margin"
            " FROM superstore"
            " GROUP BY segment"
            " ORDER BY avg_profit_margin DESC",
        ),
        (
            "Sales by month",
            "SELECT order_month, ROUND(SUM(sales), 2) AS sales"
            " FROM superstore"
            " GROUP BY order_month"
            " ORDER BY order_month",
        ),
        (
            "Count of orders with negative profit",
            "SELECT COUNT(*) AS losing_orders, ROUND(SUM(sales), 2) AS sales_at_risk"
            " FROM superstore"
            " WHERE profit < 0",
        ),
    ]

    for title, query in example_queries:
        print(f"\n=== {title} ===")
        rows = pd.read_sql_query(query, conn)
        print(rows.to_string(index=False))

print("\nSQLite database created and sample SQL queries executed.")
print("You can also open output/superstore.db with a SQLite browser or run additional queries.")
