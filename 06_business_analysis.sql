--EXCLUSIVE KPI SUMMARY
select 
round(sum(sales),2) as total_sales,
round(sum(profit),2) as total_profit,

round(100*sum(profit)/nullif(sum(sales),0),2) as profit_margin_percentage,
count(distinct order_id) as total_orders,
round(sum(sales)/count(distinct order_id),2) as average_order_value

from superstore_analytics.orders;



--PROFIT BY REGION
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


-- PROFIT BY CATEGORY/SUB-CATEGORY

SELECT
    p.category,
    p.sub_category,

    ROUND(SUM(o.sales), 2) AS total_sales,
    ROUND(SUM(o.profit), 2) AS total_profit,

    ROUND(
        100 * SUM(o.profit) / NULLIF(SUM(o.sales), 0),
        2
    ) AS profit_margin_percentage

FROM superstore_analytics.orders AS o

JOIN superstore_analytics.products AS p
    ON o.product_key = p.product_key

GROUP BY
    p.category,
    p.sub_category

ORDER BY total_profit DESC;


--TOP 10 PRODUCTS BY PROFIT
SELECT
    p.product_name,
    p.category,

    ROUND(SUM(o.sales), 2) AS total_sales,
    ROUND(SUM(o.profit), 2) AS total_profit,

    ROUND(
        100 * SUM(o.profit) / NULLIF(SUM(o.sales), 0),
        2
    ) AS profit_margin_percentage

FROM superstore_analytics.orders AS o

JOIN superstore_analytics.products AS p
    ON o.product_key = p.product_key

GROUP BY
    p.product_key,
    p.product_name,
    p.category

ORDER BY total_profit DESC

LIMIT 10;



--PRODCUTS IN LOSS

SELECT
    p.product_name,
    p.category,

    ROUND(SUM(o.sales), 2) AS total_sales,
    ROUND(SUM(o.profit), 2) AS total_profit

FROM superstore_analytics.orders AS o

JOIN superstore_analytics.products AS p
    ON o.product_key = p.product_key

GROUP BY
    p.product_key,
    p.product_name,
    p.category

HAVING SUM(o.profit) < 0

ORDER BY total_profit ASC;



--SALES BY PROFIT AND CUSTOMER SEGMENT

SELECT
    c.segment,

    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(o.sales), 2) AS total_sales,
    ROUND(SUM(o.profit), 2) AS total_profit,

    ROUND(
        SUM(o.sales) / COUNT(DISTINCT o.order_id),
        2
    ) AS average_order_value

FROM superstore_analytics.orders AS o

JOIN superstore_analytics.customers AS c
    ON o.customer_id = c.customer_id

GROUP BY c.segment

ORDER BY total_profit DESC;



--TOP 10 CUSTOMERS BY SALES

SELECT
    c.customer_name,
    c.segment,

    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(o.sales), 2) AS total_sales,
    ROUND(SUM(o.profit), 2) AS total_profit

FROM superstore_analytics.orders AS o

JOIN superstore_analytics.customers AS c
    ON o.customer_id = c.customer_id

GROUP BY
    c.customer_id,
    c.customer_name,
    c.segment

ORDER BY total_sales DESC

LIMIT 10;



--MONTHLY SALES AND PROFIT TREND

SELECT
    o.order_month,

    ROUND(SUM(o.sales), 2) AS total_sales,
    ROUND(SUM(o.profit), 2) AS total_profit,

    COUNT(DISTINCT o.order_id) AS total_orders

FROM superstore_analytics.orders AS o

GROUP BY o.order_month

ORDER BY o.order_month;