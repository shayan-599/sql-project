# ---------- Imports ----------
from pathlib import Path
from getpass import getpass

import matplotlib.pyplot as plt
import mysql.connector
import pandas as pd


# ---------- Project folders ----------
# Path(__file__) means this current Python file.
# .parent means the folder where this file is saved.
project_folder = Path(__file__).resolve().parent

# These folders will hold final outputs for GitHub.
charts_folder = project_folder / "outputs" / "charts"
tables_folder = project_folder / "outputs" / "tables"

# Create folders if they do not already exist.
charts_folder.mkdir(parents=True, exist_ok=True)
tables_folder.mkdir(parents=True, exist_ok=True)


# ---------- Helper functions ----------
def run_query(connection, query):
    """
    Send a SQL query to MySQL.
    Receive the result and return it as a pandas DataFrame.
    """
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)

    dataframe = pd.DataFrame(cursor.fetchall())

    cursor.close()
    return dataframe


def save_csv(dataframe, filename):
    """Save a pandas DataFrame as a CSV file in outputs/tables."""
    dataframe.to_csv(tables_folder / filename, index=False)


# ---------- Query 1: Executive KPI summary ----------
kpi_query = """
SELECT
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(
        100 * SUM(profit) / NULLIF(SUM(sales), 0),
        2
    ) AS profit_margin_percentage,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(
        SUM(sales) / COUNT(DISTINCT order_id),
        2
    ) AS average_order_value
FROM orders;
"""


# ---------- Query 2: Profit by region ----------
region_query = """
SELECT
    l.region,
    ROUND(SUM(o.sales), 2) AS total_sales,
    ROUND(SUM(o.profit), 2) AS total_profit,
    ROUND(
        100 * SUM(o.profit) / NULLIF(SUM(o.sales), 0),
        2
    ) AS profit_margin_percentage,
    COUNT(DISTINCT o.order_id) AS total_orders
FROM orders AS o
JOIN locations AS l
    ON o.location_key = l.location_key
GROUP BY l.region
ORDER BY total_profit DESC;
"""


# ---------- Query 3: Category and sub-category profit ----------
category_query = """
SELECT
    p.category,
    p.sub_category,
    ROUND(SUM(o.sales), 2) AS total_sales,
    ROUND(SUM(o.profit), 2) AS total_profit,
    ROUND(
        100 * SUM(o.profit) / NULLIF(SUM(o.sales), 0),
        2
    ) AS profit_margin_percentage
FROM orders AS o
JOIN products AS p
    ON o.product_key = p.product_key
GROUP BY
    p.category,
    p.sub_category
ORDER BY total_profit DESC;
"""


# ---------- Query 4: Top 10 products by profit ----------
top_products_query = """
SELECT
    p.product_name,
    p.category,
    ROUND(SUM(o.sales), 2) AS total_sales,
    ROUND(SUM(o.profit), 2) AS total_profit,
    ROUND(
        100 * SUM(o.profit) / NULLIF(SUM(o.sales), 0),
        2
    ) AS profit_margin_percentage
FROM orders AS o
JOIN products AS p
    ON o.product_key = p.product_key
GROUP BY
    p.product_key,
    p.product_name,
    p.category
ORDER BY total_profit DESC
LIMIT 10;
"""


# ---------- Query 5: Loss-making products ----------
loss_products_query = """
SELECT
    p.product_name,
    p.category,
    ROUND(SUM(o.sales), 2) AS total_sales,
    ROUND(SUM(o.profit), 2) AS total_profit
FROM orders AS o
JOIN products AS p
    ON o.product_key = p.product_key
GROUP BY
    p.product_key,
    p.product_name,
    p.category
HAVING SUM(o.profit) < 0
ORDER BY total_profit ASC;
"""


# ---------- Query 6: Customer segment performance ----------
segment_query = """
SELECT
    c.segment,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(o.sales), 2) AS total_sales,
    ROUND(SUM(o.profit), 2) AS total_profit,
    ROUND(
        SUM(o.sales) / COUNT(DISTINCT o.order_id),
        2
    ) AS average_order_value
FROM orders AS o
JOIN customers AS c
    ON o.customer_id = c.customer_id
GROUP BY c.segment
ORDER BY total_profit DESC;
"""


# ---------- Query 7: Top 10 customers by sales ----------
top_customers_query = """
SELECT
    c.customer_name,
    c.segment,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(o.sales), 2) AS total_sales,
    ROUND(SUM(o.profit), 2) AS total_profit
FROM orders AS o
JOIN customers AS c
    ON o.customer_id = c.customer_id
GROUP BY
    c.customer_id,
    c.customer_name,
    c.segment
ORDER BY total_sales DESC
LIMIT 10;
"""


# ---------- Query 8: Monthly sales and profit ----------
monthly_query = """
SELECT
    o.order_month,
    ROUND(SUM(o.sales), 2) AS total_sales,
    ROUND(SUM(o.profit), 2) AS total_profit,
    COUNT(DISTINCT o.order_id) AS total_orders
FROM orders AS o
GROUP BY o.order_month
ORDER BY o.order_month;
"""


# ---------- Connect to MySQL ----------
# getpass hides your password while you type it.
password = getpass("Enter your MySQL password: ")

connection = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password=password,
    database="superstore_analytics"
)

try:
    # ---------- Run all eight queries ----------
    df_kpi = run_query(connection, kpi_query)
    df_region = run_query(connection, region_query)
    df_category = run_query(connection, category_query)
    df_products = run_query(connection, top_products_query)
    df_loss_products = run_query(connection, loss_products_query)
    df_segment = run_query(connection, segment_query)
    df_top_customers = run_query(connection, top_customers_query)
    df_monthly = run_query(connection, monthly_query)

    # ---------- Save all query results as CSV ----------
    save_csv(df_kpi, "executive_summary.csv")
    save_csv(df_region, "profit_by_region.csv")
    save_csv(df_category, "category_profit.csv")
    save_csv(df_products, "top_products.csv")
    save_csv(df_loss_products, "loss_making_products.csv")
    save_csv(df_segment, "customer_segment_performance.csv")
    save_csv(df_top_customers, "top_customers.csv")
    save_csv(df_monthly, "monthly_sales_profit.csv")

    # Print KPIs in the terminal for a quick check.
    print("\nExecutive KPI summary:")
    print(df_kpi.to_string(index=False))

    # Convert MySQL number values into normal Python numbers for matplotlib.
    for dataframe in [df_region, df_category, df_products, df_monthly]:
        for column in ["total_sales", "total_profit"]:
            dataframe[column] = pd.to_numeric(dataframe[column])

    # ---------- Chart 1: Profit by region ----------
    region_chart = df_region.sort_values("total_profit")

    fig, ax = plt.subplots(figsize=(9, 5))

    bars = ax.barh(
        region_chart["region"],
        region_chart["total_profit"],
        color="#2563EB"
    )

    ax.bar_label(
        bars,
        labels=[
            f"${value:,.0f}"
            for value in region_chart["total_profit"]
        ],
        padding=4
    )

    ax.set_title("Total Profit by Region", fontweight="bold")
    ax.set_xlabel("Profit (USD)")
    ax.set_ylabel("Region")

    fig.tight_layout()
    fig.savefig(charts_folder / "profit_by_region.png", dpi=180)
    plt.close(fig)

    # ---------- Chart 2: Profit by category and sub-category ----------
    category_chart = df_category.sort_values("total_profit").copy()

    category_chart["label"] = (
        category_chart["category"]
        + " - "
        + category_chart["sub_category"]
    )

    # Losses are red; profitable groups are green.
    colors = [
        "#DC2626" if value < 0 else "#16A34A"
        for value in category_chart["total_profit"]
    ]

    fig, ax = plt.subplots(figsize=(11, 7))

    ax.barh(
        category_chart["label"],
        category_chart["total_profit"],
        color=colors
    )

    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_title(
        "Profit by Category and Sub-Category",
        fontweight="bold"
    )
    ax.set_xlabel("Profit (USD)")
    ax.set_ylabel("Product group")

    fig.tight_layout()
    fig.savefig(charts_folder / "category_profit.png", dpi=180)
    plt.close(fig)

    # ---------- Chart 3: Top 10 products by profit ----------
    products_chart = df_products.sort_values("total_profit")

    fig, ax = plt.subplots(figsize=(11, 6))

    bars = ax.barh(
        products_chart["product_name"],
        products_chart["total_profit"],
        color="#F97316"
    )

    ax.bar_label(
        bars,
        labels=[
            f"${value:,.0f}"
            for value in products_chart["total_profit"]
        ],
        padding=3,
        fontsize=8
    )

    ax.set_title("Top 10 Products by Profit", fontweight="bold")
    ax.set_xlabel("Profit (USD)")
    ax.set_ylabel("Product")

    fig.tight_layout()
    fig.savefig(charts_folder / "top_products_by_profit.png", dpi=180)
    plt.close(fig)

    # ---------- Chart 4: Monthly sales and profit ----------
    df_monthly["order_month"] = pd.to_datetime(df_monthly["order_month"])

    fig, ax_sales = plt.subplots(figsize=(12, 6))

    sales_line = ax_sales.plot(
        df_monthly["order_month"],
        df_monthly["total_sales"],
        color="#2563EB",
        linewidth=2.5,
        marker="o",
        label="Sales"
    )

    ax_sales.set_xlabel("Month")
    ax_sales.set_ylabel("Sales (USD)", color="#2563EB")
    ax_sales.tick_params(axis="y", labelcolor="#2563EB")

    # A second y-axis lets profit stay visible beside much larger sales values.
    ax_profit = ax_sales.twinx()

    profit_line = ax_profit.plot(
        df_monthly["order_month"],
        df_monthly["total_profit"],
        color="#16A34A",
        linewidth=2.5,
        marker="o",
        label="Profit"
    )

    ax_profit.set_ylabel("Profit (USD)", color="#16A34A")
    ax_profit.tick_params(axis="y", labelcolor="#16A34A")

    ax_sales.set_title("Monthly Sales and Profit Trend", fontweight="bold")

    lines = sales_line + profit_line
    labels = [line.get_label() for line in lines]
    ax_sales.legend(lines, labels, loc="upper left")

    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(charts_folder / "monthly_sales_profit.png", dpi=180)
    plt.close(fig)

finally:
    # Always close the database connection after the script finishes.
    connection.close()


print("\nDone!")
print("CSV tables saved in:", tables_folder)
print("Charts saved in:", charts_folder)
