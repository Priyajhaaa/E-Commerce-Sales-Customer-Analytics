-- ============================================================
-- E-COMMERCE SALES & CUSTOMER ANALYTICS
-- SQL Analysis Project
-- PostgreSQL
-- ============================================================


-- ============================================================
-- SECTION 1: BASIC DATA UNDERSTANDING
-- ============================================================

-- 1. Total Customers
SELECT COUNT(*) AS total_customers
FROM customers;


-- 2. Total Products
SELECT COUNT(*) AS total_products
FROM products;


-- 3. Total Orders
SELECT COUNT(*) AS total_orders
FROM orders;


-- 4. Total Order Items
SELECT COUNT(*) AS total_order_items
FROM order_items;


-- 5. Total Payments
SELECT COUNT(*) AS total_payments
FROM payments;


-- 6. Distinct Product Categories
SELECT DISTINCT category
FROM products
ORDER BY category;


-- ============================================================
-- SECTION 2: ORDER ANALYSIS
-- ============================================================

-- 7. Order Status Distribution
SELECT
    order_status,
    COUNT(*) AS order_count
FROM orders
GROUP BY order_status
ORDER BY order_count DESC;


-- 8. Completed Orders
SELECT COUNT(*) AS completed_orders
FROM orders
WHERE order_status = 'Completed';


-- 9. Failed Orders
SELECT COUNT(*) AS failed_orders
FROM orders
WHERE order_status = 'Failed';


-- 10. Refunded Orders
SELECT COUNT(*) AS refunded_orders
FROM orders
WHERE order_status = 'Refunded';


-- 11. Completion Rate
SELECT
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE order_status = 'Completed'
        ) / COUNT(*),
        2
    ) AS completion_rate
FROM orders;


-- 12. Refund Rate
SELECT
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE order_status = 'Refunded'
        ) / COUNT(*),
        2
    ) AS refund_rate
FROM orders;


-- ============================================================
-- SECTION 3: REVENUE ANALYSIS
-- ============================================================

-- 13. Total Revenue
SELECT
    ROUND(
        SUM(quantity * unit_price * (1 - discount)),
        2
    ) AS total_revenue
FROM order_items;


-- 14. Revenue by Category
SELECT
    p.category,
    ROUND(
        SUM(
            oi.quantity *
            oi.unit_price *
            (1 - oi.discount)
        ),
        2
    ) AS revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY revenue DESC;


-- 15. Revenue by Product
SELECT
    p.product_id,
    p.product_name,
    ROUND(
        SUM(
            oi.quantity *
            oi.unit_price *
            (1 - oi.discount)
        ),
        2
    ) AS revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY
    p.product_id,
    p.product_name
ORDER BY revenue DESC;


-- 16. Top 10 Products by Revenue
SELECT
    p.product_id,
    p.product_name,
    p.category,
    ROUND(
        SUM(
            oi.quantity *
            oi.unit_price *
            (1 - oi.discount)
        ),
        2
    ) AS revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category
ORDER BY revenue DESC
LIMIT 10;


-- 17. Quantity Sold by Category
SELECT
    p.category,
    SUM(oi.quantity) AS total_quantity_sold
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY total_quantity_sold DESC;


-- ============================================================
-- SECTION 4: GEOGRAPHIC ANALYSIS
-- ============================================================

-- 18. State-wise Revenue
SELECT
    o.shipping_state,
    ROUND(
        SUM(
            oi.quantity *
            oi.unit_price *
            (1 - oi.discount)
        ),
        2
    ) AS revenue
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY o.shipping_state
ORDER BY revenue DESC;


-- 19. Top 10 States by Revenue
SELECT
    o.shipping_state,
    ROUND(
        SUM(
            oi.quantity *
            oi.unit_price *
            (1 - oi.discount)
        ),
        2
    ) AS revenue
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY o.shipping_state
ORDER BY revenue DESC
LIMIT 10;


-- ============================================================
-- SECTION 5: TIME-BASED ANALYSIS
-- ============================================================

-- 20. Monthly Revenue
SELECT
    DATE_TRUNC('month', o.order_date) AS month,
    ROUND(
        SUM(
            oi.quantity *
            oi.unit_price *
            (1 - oi.discount)
        ),
        2
    ) AS revenue
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY month
ORDER BY month;


-- 21. Year-wise Revenue
SELECT
    EXTRACT(YEAR FROM o.order_date) AS year,
    ROUND(
        SUM(
            oi.quantity *
            oi.unit_price *
            (1 - oi.discount)
        ),
        2
    ) AS revenue
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY year
ORDER BY year;


-- 22. Monthly Order Count
SELECT
    DATE_TRUNC('month', order_date) AS month,
    COUNT(*) AS total_orders
FROM orders
GROUP BY month
ORDER BY month;


-- 23. Year-wise Order Count
SELECT
    EXTRACT(YEAR FROM order_date) AS year,
    COUNT(*) AS total_orders
FROM orders
GROUP BY year
ORDER BY year;


-- ============================================================
-- SECTION 6: PAYMENT ANALYSIS
-- ============================================================

-- 24. Payment Method Distribution
SELECT
    payment_method,
    COUNT(*) AS payment_count
FROM payments
GROUP BY payment_method
ORDER BY payment_count DESC;


-- 25. Revenue / Amount by Payment Method
SELECT
    payment_method,
    COUNT(*) AS payment_count,
    ROUND(SUM(amount), 2) AS total_amount
FROM payments
GROUP BY payment_method
ORDER BY total_amount DESC;


-- 26. Average Payment Amount by Method
SELECT
    payment_method,
    ROUND(AVG(amount), 2) AS average_payment
FROM payments
GROUP BY payment_method
ORDER BY average_payment DESC;


-- ============================================================
-- SECTION 7: CUSTOMER ANALYSIS
-- ============================================================

-- 27. Customer-wise Revenue
SELECT
    o.customer_id,
    ROUND(
        SUM(
            oi.quantity *
            oi.unit_price *
            (1 - oi.discount)
        ),
        2
    ) AS revenue
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY o.customer_id
ORDER BY revenue DESC;


-- 28. Top 10 Customers by Revenue
SELECT
    o.customer_id,
    ROUND(
        SUM(
            oi.quantity *
            oi.unit_price *
            (1 - oi.discount)
        ),
        2
    ) AS revenue
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY o.customer_id
ORDER BY revenue DESC
LIMIT 10;


-- 29. Orders per Customer
SELECT
    customer_id,
    COUNT(*) AS total_orders
FROM orders
GROUP BY customer_id
ORDER BY total_orders DESC;


-- 30. Customer Revenue Segmentation
WITH customer_revenue AS (
    SELECT
        o.customer_id,
        SUM(
            oi.quantity *
            oi.unit_price *
            (1 - oi.discount)
        ) AS revenue
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    WHERE o.order_status = 'Completed'
    GROUP BY o.customer_id
)

SELECT
    CASE
        WHEN revenue < 50000
            THEN 'Low Value'
        WHEN revenue < 200000
            THEN 'Medium Value'
        ELSE 'High Value'
    END AS customer_segment,

    COUNT(*) AS customer_count

FROM customer_revenue

GROUP BY
    CASE
        WHEN revenue < 50000
            THEN 'Low Value'
        WHEN revenue < 200000
            THEN 'Medium Value'
        ELSE 'High Value'
    END

ORDER BY customer_count DESC;


-- ============================================================
-- SECTION 8: ADVANCED SQL ANALYSIS
-- ============================================================

-- 31. Rank Products by Revenue
WITH product_revenue AS (
    SELECT
        p.product_id,
        p.product_name,
        SUM(
            oi.quantity *
            oi.unit_price *
            (1 - oi.discount)
        ) AS revenue
    FROM order_items oi
    JOIN products p
        ON oi.product_id = p.product_id
    GROUP BY
        p.product_id,
        p.product_name
)

SELECT
    product_id,
    product_name,
    ROUND(revenue, 2) AS revenue,
    RANK() OVER (
        ORDER BY revenue DESC
    ) AS revenue_rank
FROM product_revenue
ORDER BY revenue_rank;


-- 32. Monthly Revenue with Previous Month Revenue
WITH monthly_revenue AS (
    SELECT
        DATE_TRUNC('month', o.order_date) AS month,
        SUM(
            oi.quantity *
            oi.unit_price *
            (1 - oi.discount)
        ) AS revenue
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY month
)

SELECT
    month,
    ROUND(revenue, 2) AS revenue,
    ROUND(
        LAG(revenue) OVER (
            ORDER BY month
        ),
        2
    ) AS previous_month_revenue
FROM monthly_revenue
ORDER BY month;


-- 33. Monthly Revenue Growth %
WITH monthly_revenue AS (
    SELECT
        DATE_TRUNC('month', o.order_date) AS month,
        SUM(
            oi.quantity *
            oi.unit_price *
            (1 - oi.discount)
        ) AS revenue
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY month
),

revenue_with_previous AS (
    SELECT
        month,
        revenue,
        LAG(revenue) OVER (
            ORDER BY month
        ) AS previous_revenue
    FROM monthly_revenue
)

SELECT
    month,
    ROUND(revenue, 2) AS revenue,
    ROUND(
        100.0 *
        (revenue - previous_revenue)
        / NULLIF(previous_revenue, 0),
        2
    ) AS growth_percentage
FROM revenue_with_previous
ORDER BY month;


-- ============================================================
-- END OF E-COMMERCE SALES & CUSTOMER ANALYTICS
-- ============================================================
