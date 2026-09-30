SELECT region, 
       SUM(amount) AS total_revenue,
       COUNT(*) AS order_count
FROM large.orders
WHERE order_date BETWEEN '2023-06-01' AND '2023-06-30'
GROUP BY region
ORDER BY total_revenue DESC;