DROP TABLE IF EXISTS superstore_analytics.locations;

CREATE TABLE superstore_analytics.locations (
    location_key INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    region VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,

    UNIQUE (city, state, region, postal_code)
);

INSERT INTO superstore_analytics.locations (
    city,
    state,
    region,
    postal_code
)
SELECT DISTINCT
    city,
    state,
    region,
    postal_code
FROM superstore_analytics.stg_superstore_clean;

SELECT *
FROM superstore_analytics.locations
LIMIT 20;

SELECT COUNT(*) AS location_count
FROM superstore_analytics.locations;