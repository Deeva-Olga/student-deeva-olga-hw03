SELECT region, 
       SUM(amount) AS total_revenue,
       COUNT(*) AS order_count
FROM large.orders
WHERE order_date BETWEEN '2022-01-01' AND '2023-12-31'
GROUP BY region
ORDER BY total_revenue DESC;