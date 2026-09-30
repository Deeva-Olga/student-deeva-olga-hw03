import psycopg2
import time

conn = psycopg2.connect(host="localhost", database="dwh", user="airflow", password="airflow")
conn.autocommit = True
cur = conn.cursor()

# Обновляем статистику перед замерами
cur.execute("ANALYZE large.orders;")

queries = {
    "narrow": """
        SELECT region, SUM(amount), COUNT(*)
        FROM large.orders
        WHERE order_date BETWEEN '2023-06-01' AND '2023-06-30'
        GROUP BY region ORDER BY SUM(amount) DESC;
    """,
    "wide": """
        SELECT region, SUM(amount), COUNT(*)
        FROM large.orders
        WHERE order_date BETWEEN '2022-01-01' AND '2023-12-31'
        GROUP BY region ORDER BY SUM(amount) DESC;
    """
}

# Прогрев (1 раз, не считаем)
for name, sql in queries.items():
    cur.execute(sql)
    cur.fetchall()

# 5 измеряемых повторов
for name, sql in queries.items():
    times = []
    for i in range(5):
        start = time.perf_counter()
        cur.execute(sql)
        cur.fetchall()
        elapsed = (time.perf_counter() - start) * 1000  # мс
        times.append(elapsed)
        print(f"{name} run {i+1}: {elapsed:.2f} ms")
    
    median = sorted(times)[2]
    print(f"  -> Медиана {name}: {median:.2f} ms\n")

cur.close()
conn.close()
