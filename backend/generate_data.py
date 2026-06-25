import mysql.connector
from datetime import datetime, timedelta
import random

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="company_ai",
    port=3307
)

cursor = conn.cursor()

# 🔥 Reset table
cursor.execute("TRUNCATE TABLE sales")

start_date = datetime(2025, 1, 1)

# 🔥 CHANGE FOR PERFORMANCE TEST
NUM_DAYS = 365   # 1 year (Day 22 requirement)

NUM_PRODUCTS = 5
NUM_CUSTOMERS = 5
NUM_EMPLOYEES = 5

for i in range(NUM_DAYS):

    current_date = start_date + timedelta(days=i)

    base_sales = 1000 + (i * 25)
    noise = random.randint(-100, 200)

    sales_amount = max(500, base_sales + noise)

    product_id = random.randint(1, NUM_PRODUCTS)
    customer_id = random.randint(1, NUM_CUSTOMERS)
    employee_id = random.randint(1, NUM_EMPLOYEES)

    cursor.execute("""
        INSERT INTO sales (product_id, customer_id, employee_id, sales_amount, sale_date)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        product_id,
        customer_id,
        employee_id,
        sales_amount,
        current_date.strftime('%Y-%m-%d')
    ))

conn.commit()

print("✅ Large dataset (1 year) inserted successfully!")

cursor.close()
conn.close()