DROP TABLE IF EXISTS superstore_analytics.products;

CREATE TABLE superstore_analytics.products (
    
    -- MySQL creates a new unique number for every product record
    product_key INT AUTO_INCREMENT PRIMARY KEY,

    -- Original ID from the CSV; it is not always unique
    product_id VARCHAR(30) NOT NULL,

    -- Stable product details
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    sub_category VARCHAR(100) NOT NULL,

    -- Together, these fields identify one distinct product definition
    UNIQUE (product_id, product_name, category, sub_category)
);

INSERT INTO superstore_analytics.products (
    product_id,
    product_name,
    category,
    sub_category
)
SELECT DISTINCT
    product_id,
    product_name,
    category,
    sub_category
FROM superstore_analytics.stg_superstore_clean;