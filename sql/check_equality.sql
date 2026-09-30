-- Узкий: результат до индекса vs после (одинаковые запросы → 0 diff)
SELECT 'narrow_diff' AS check_name, COUNT(*) AS diff_rows
FROM (
    (SELECT region, SUM(amount) AS total_revenue, COUNT(*) AS order_count
     FROM large.orders
     WHERE order_date BETWEEN '2023-06-01' AND '2023-06-30'
     GROUP BY region)
    EXCEPT ALL
    (SELECT region, SUM(amount) AS total_revenue, COUNT(*) AS order_count
     FROM large.orders
     WHERE order_date BETWEEN '2023-06-01' AND '2023-06-30'
     GROUP BY region)
) AS diff
UNION ALL
SELECT 'wide_diff', COUNT(*)
FROM (
    (SELECT region, SUM(amount) AS total_revenue, COUNT(*) AS order_count
     FROM large.orders
     WHERE order_date BETWEEN '2022-01-01' AND '2023-12-31'
     GROUP BY region)
    EXCEPT ALL
    (SELECT region, SUM(amount) AS total_revenue, COUNT(*) AS order_count
     FROM large.orders
     WHERE order_date BETWEEN '2022-01-01' AND '2023-12-31'
     GROUP BY region)
) AS diff;
