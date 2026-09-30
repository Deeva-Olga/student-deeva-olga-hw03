EXPLAIN (ANALYZE, BUFFERS) 
SELECT region, SUM(amount), COUNT(*)
FROM large.orders
WHERE order_date BETWEEN '2022-01-01' AND '2023-12-31'
GROUP BY region ORDER BY SUM(amount) DESC;