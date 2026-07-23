DROP TABLE IF EXISTS superstore_analytics.orders;

CREATE TABLE superstore_analytics.orders (
    row_id INT PRIMARY KEY,
    order_id VARCHAR(30) NOT NULL,
    order_date DATE NOT NULL,
    ship_date DATE NOT NULL,
    ship_mode VARCHAR(50) NOT NULL,

    customer_id VARCHAR(30) NOT NULL,
    product_key INT NOT NULL,
    location_key INT NOT NULL,

    sales DECIMAL(12, 2) NOT NULL,
    quantity INT NOT NULL,
    discount DECIMAL(5, 2) NOT NULL,
    profit DECIMAL(12, 2) NOT NULL,

    shipping_days INT NOT NULL,
    profit_margin DECIMAL(12, 6) NOT NULL,
    order_year INT NOT NULL,
    order_month_num INT NOT NULL,
    order_day_of_week VARCHAR(20) NOT NULL,
    order_month VARCHAR(20) NOT NULL,

    FOREIGN KEY (customer_id)
        REFERENCES superstore_analytics.customers(customer_id),

    FOREIGN KEY (product_key)
        REFERENCES superstore_analytics.products(product_key),

    FOREIGN KEY (location_key)
        REFERENCES superstore_analytics.locations(location_key)
);


INSERT INTO superstore_analytics.orders (
    row_id,
    order_id,
    order_date,
    ship_date,
    ship_mode,
    customer_id,
    product_key,
    location_key,
    sales,
    quantity,
    discount,
    profit,
    shipping_days,
    profit_margin,
    order_year,
    order_month_num,
    order_day_of_week,
    order_month
)
SELECT
    s.row_id,
    s.order_id,
    s.order_date,
    s.ship_date,
    s.ship_mode,
    s.customer_id,
    p.product_key,
    l.location_key,
    s.sales,
    s.quantity,
    s.discount,
    s.profit,
    s.shipping_days,
    s.profit_margin,
    s.order_year,
    s.order_month_num,
    s.order_day_of_week,
    s.order_month
FROM superstore_analytics.stg_superstore_clean s
JOIN superstore_analytics.products p
    ON s.product_id = p.product_id
    AND s.product_name = p.product_name
    AND s.category = p.category
    AND s.sub_category = p.sub_category
JOIN superstore_analytics.locations l
    ON s.city = l.city
    AND s.state = l.state
    AND s.region = l.region
    AND s.postal_code = l.postal_code;


SELECT COUNT(*) AS orders_loaded
FROM superstore_analytics.orders;