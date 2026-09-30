CREATE INDEX IF NOT EXISTS idx_orders_order_date ON large.orders (order_date);
ANALYZE large.orders;