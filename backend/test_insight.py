from db_connection import connect_db
from postgres_connection import connect_postgres
from insight_engine import InsightEngine

engine = InsightEngine()


# ---------- MYSQL TEST ----------
def test_mysql_insights():

    connection = connect_db()
    cursor = connection.cursor()

    # SALES
    cursor.execute("SELECT * FROM sales")
    sales_data = cursor.fetchall()
    print("\nSALES INSIGHT")
    print(engine.sales_insight(sales_data))

    # CUSTOMERS
    cursor.execute("SELECT * FROM customers")
    customer_data = cursor.fetchall()
    print("\nCUSTOMER INSIGHT")
    print(engine.customer_insight(customer_data))

    # PRODUCTS
    cursor.execute("SELECT * FROM products")
    product_data = cursor.fetchall()
    print("\nPRODUCT INSIGHT")
    print(engine.product_insight(product_data))

    # EMPLOYEES
    cursor.execute("SELECT * FROM employees")
    employee_data = cursor.fetchall()
    print("\nEMPLOYEE INSIGHT")
    print(engine.employee_insight(employee_data))

    cursor.close()
    connection.close()


# ---------- POSTGRES TEST ----------
def test_postgres_insights():

    connection = connect_postgres()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM finance")
    finance_data = cursor.fetchall()

    print("\nFINANCE INSIGHT")
    print(engine.finance_insight(finance_data))

    cursor.close()
    connection.close()


# ---------- FILE TEST ----------
def test_file_insights():

    print("\nCSV INSIGHT")
    print(engine.csv_insight("files/sample.csv"))

    print("\nEXCEL INSIGHT")
    print(engine.excel_insight("files/samp.xlsx"))

    pdf_text = "AI BI System Report Employee Sales Data John 2000 Mary 3500 David 4000"

    print("\nPDF INSIGHT")
    print(engine.pdf_insight(pdf_text))


# ---------- MAIN ----------
if __name__ == "__main__":

    test_mysql_insights()

    test_postgres_insights()

    test_file_insights()