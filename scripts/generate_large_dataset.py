import psycopg2
import random
from datetime import datetime, timedelta

random.seed(42)  # Воспроизводимость

conn = psycopg2.connect(host="localhost", database="dwh", user="airflow", password="airflow")
cur = conn.cursor()

# Создаём схему для большого набора
cur.execute("CREATE SCHEMA IF NOT EXISTS large;")

# Таблица заказов (без клиентов для простоты измерений)
cur.execute("""
    DROP TABLE IF EXISTS large.orders CASCADE;
    CREATE TABLE large.orders (
        order_id      BIGSERIAL PRIMARY KEY,
        order_date    DATE NOT NULL,
        region        VARCHAR(20) NOT NULL,
        amount        NUMERIC(10,2) NOT NULL,
        quantity      INT NOT NULL
    );
""")

# Параметры генерации
regions = ['North', 'South', 'East', 'West', 'Central']
weights = [0.30, 0.25, 0.20, 0.15, 0.10]  # Неравномерное распределение

start_date = datetime(2022, 1, 1)
end_date = datetime(2023, 12, 31)
total_days = (end_date - start_date).days + 1

BATCH_SIZE = 10000
TOTAL_ROWS = 500000

print(f"Генерация {TOTAL_ROWS} заказов...")

for batch in range(0, TOTAL_ROWS, BATCH_SIZE):
    rows = []
    for _ in range(BATCH_SIZE):
        # Случайная дата с небольшим трендом (больше заказов в 2023)
        day_offset = random.randint(0, total_days - 1)
        order_date = start_date + timedelta(days=day_offset)
        
        # Взвешенный выбор региона
        region = random.choices(regions, weights=weights, k=1)[0]
        
        # Сумма: нормальное распределение вокруг 150, от 10 до 1000
        amount = max(10.0, min(1000.0, random.gauss(150, 80)))
        amount = round(amount, 2)
        
        quantity = random.randint(1, 5)
        
        rows.append((order_date, region, amount, quantity))
    
    # Массовая вставка
    from psycopg2.extras import execute_values
    execute_values(cur, 
        "INSERT INTO large.orders (order_date, region, amount, quantity) VALUES %s",
        rows)
    conn.commit()
    print(f"  Вставлено: {min(batch + BATCH_SIZE, TOTAL_ROWS)} / {TOTAL_ROWS}")

# Обновляем статистику
cur.execute("ANALYZE large.orders;")
conn.commit()

# Итоговая проверка
cur.execute("SELECT count(*), min(order_date), max(order_date) FROM large.orders;")
print(f"\nИтог: {cur.fetchone()}")

cur.close()
conn.close()
print("Генерация завершена.")