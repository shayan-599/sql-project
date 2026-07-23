SELECT
    l.region,

    ROUND(SUM(o.sales), 2) AS total_sales,
    ROUND(SUM(o.profit), 2) AS total_profit,

    ROUND(
        100 * SUM(o.profit) / NULLIF(SUM(o.sales), 0),
        2
    ) AS profit_margin_percentage,

    COUNT(DISTINCT o.order_id) AS total_orders

FROM superstore_analytics.orders AS o

JOIN superstore_analytics.locations AS l
    ON o.location_key = l.location_key

GROUP BY l.region

ORDER BY total_profit DESC;
