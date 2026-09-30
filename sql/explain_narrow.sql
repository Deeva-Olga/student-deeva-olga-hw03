EXPLAIN (ANALYZE, BUFFERS) 
SELECT region, SUM(amount), COUNT(*)
FROM large.orders
WHERE order_date BETWEEN '2023-06-01' AND '2023-06-30'
GROUP BY region ORDER BY SUM(amount) DESC;