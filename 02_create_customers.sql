-- Create a table that stores each customer once
DROP TABLE IF EXISTS superstore_analytics.customers;

CREATE TABLE superstore_analytics.customers (
    customer_id VARCHAR(30) PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    segment VARCHAR(30) NOT NULL
);

-- Insert only unique customer records from staging data
INSERT INTO superstore_analytics.customers (
    customer_id,
    customer_name,
    segment
)
SELECT DISTINCT
    customer_id,
    customer_name,
    segment
FROM superstore_analytics.stg_superstore_clean;