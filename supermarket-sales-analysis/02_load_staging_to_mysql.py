from pathlib import Path
from getpass import getpass

import pandas as pd
import mysql.connector


# Find the cleaned CSV relative to this Python file
project_folder = Path(__file__).resolve().parent
csv_path = project_folder / "output" / "cleaned_superstore_data.csv"

# Read cleaned data
df = pd.read_csv(csv_path)

# Convert CSV date text back into proper Python dates
df["order_date"] = pd.to_datetime(df["order_date"]).dt.date
df["ship_date"] = pd.to_datetime(df["ship_date"]).dt.date

# Postal codes should be text, not numbers
df["postal_code"] = df["postal_code"].astype("string")

# Connect to your local MySQL database
password = getpass("Enter your MySQL root password: ")

connection = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password=password,
    database="superstore_analytics"
)

cursor = connection.cursor()

# This removes only the staging table if you run the script again
cursor.execute("DROP TABLE IF EXISTS stg_superstore_clean")

# Create the staging table
cursor.execute("""
    CREATE TABLE stg_superstore_clean (
        row_id INT PRIMARY KEY,
        order_id VARCHAR(30),
        order_date DATE,
        ship_date DATE,
        ship_mode VARCHAR(50),
        customer_id VARCHAR(30),
        customer_name VARCHAR(100),
        segment VARCHAR(50),
        country VARCHAR(50),
        city VARCHAR(100),
        state VARCHAR(100),
        postal_code VARCHAR(20),
        region VARCHAR(50),
        product_id VARCHAR(30),
        category VARCHAR(100),
        sub_category VARCHAR(100),
        product_name VARCHAR(255),
        sales DECIMAL(12, 2),
        quantity INT,
        discount DECIMAL(5, 2),
        profit DECIMAL(12, 2),
        shipping_days INT,
        profit_margin DECIMAL(12, 6),
        order_year INT,
        order_month_num INT,
        order_day_of_week VARCHAR(20),
        order_month VARCHAR(10)
    )
""")

# Insert every cleaned CSV row into MySQL
columns = list(df.columns)
placeholders = ", ".join(["%s"] * len(columns))

insert_query = f"""
    INSERT INTO stg_superstore_clean ({", ".join(columns)})
    VALUES ({placeholders})
"""

records = []
for row in df.itertuples(index=False, name=None):
    cleaned_row = []

    for value in row:
        if pd.isna(value):
            cleaned_row.append(None)
        elif hasattr(value, "item"):
            cleaned_row.append(value.item())
        else:
            cleaned_row.append(value)

    records.append(tuple(cleaned_row))

cursor.executemany(insert_query, records)
connection.commit()

print(f"Successfully loaded {len(df):,} rows into stg_superstore_clean.")

cursor.close()
connection.close()