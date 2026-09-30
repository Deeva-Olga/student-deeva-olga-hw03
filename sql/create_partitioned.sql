-- Секционированная таблица по месяцам
DROP TABLE IF EXISTS large.orders_partitioned CASCADE;

CREATE TABLE large.orders_partitioned (
    order_id    BIGSERIAL,
    order_date   DATE NOT NULL,
    region      VARCHAR(20) NOT NULL,
    amount      NUMERIC(10,2) NOT NULL,
    quantity    INT NOT NULL,
    PRIMARY KEY (order_id, order_date)
) PARTITION BY RANGE (order_date);

-- 24 партиции на 2022-2023
DO $$
DECLARE
    d DATE := '2022-01-01';
    part_name TEXT;
BEGIN
    WHILE d < '2024-01-01' LOOP
        part_name := 'orders_p_' || to_char(d, 'YYYY_MM');
        EXECUTE format(
            'CREATE TABLE large.%I PARTITION OF large.orders_partitioned
             FOR VALUES FROM (%L) TO (%L)',
            part_name, d, (d + INTERVAL '1 month')::DATE
        );
        d := (d + INTERVAL '1 month')::DATE;
    END LOOP;
END $$;

-- Индекс на секционированной таблице (создастся на каждой секции)
CREATE INDEX idx_part_order_date ON large.orders_partitioned (order_date);

-- Копируем данные
INSERT INTO large.orders_partitioned (order_id, order_date, region, amount, quantity)
SELECT order_id, order_date, region, amount, quantity FROM large.orders;

ANALYZE large.orders_partitioned;

-- Проверка числа строк
SELECT
    (SELECT COUNT(*) FROM large.orders) AS source_rows,
    (SELECT COUNT(*) FROM large.orders_partitioned) AS partitioned_rows;
