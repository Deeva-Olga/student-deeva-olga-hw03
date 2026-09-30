import pandas as pd
import psycopg2

def load_to_raw():
    conn = psycopg2.connect(host="localhost", database="dwh", user="airflow", password="airflow")
    cur = conn.cursor()
    
    cur.execute("CREATE SCHEMA IF NOT EXISTS raw;")
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS raw.customers (
            customer_id INT, name VARCHAR, region VARCHAR, status VARCHAR, updated_at TIMESTAMP
        );
        TRUNCATE TABLE raw.customers;
    """)
    
    df_cust = pd.read_csv('/home/deeva/dwh_homework/data/raw_customers.csv')
    for index, row in df_cust.iterrows():
        cur.execute("INSERT INTO raw.customers VALUES (%s, %s, %s, %s, %s)",
            (int(row['customer_id']), row['name'], row['region'], row['status'], row['updated_at']))

    cur.execute("""
        CREATE TABLE IF NOT EXISTS raw.orders (
            order_id INT, customer_id INT, order_date DATE, amount NUMERIC, quantity INT
        );
        TRUNCATE TABLE raw.orders;
    """)
    
    df_ord = pd.read_csv('/home/deeva/dwh_homework/data/raw_orders.csv')
    for index, row in df_ord.iterrows():
        cur.execute("INSERT INTO raw.orders VALUES (%s, %s, %s, %s, %s)",
            (int(row['order_id']), int(row['customer_id']), row['order_date'], float(row['amount']), int(row['quantity'])))

    conn.commit()
    cur.close()
    conn.close()
    print("Raw data loaded successfully.")

if __name__ == "__main__":
    load_to_raw()
