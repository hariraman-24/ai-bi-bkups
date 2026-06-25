import mysql.connector
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # XAMPP default password
            database="company_ai",
            port=3307
        )
        if connection.is_connected():
            print("Connected to MySQL database successfully")
        return connection
    except mysql.connector.Error as err:
        print("Error:", err)
def fetch_customers():
    connection = connect_db()
    cursor = connection.cursor()
    query = "SELECT * FROM employees"
    cursor.execute(query)
    results = cursor.fetchall()
    print("\nEmployees Table Data:\n")

    for row in results:
        print(row)
    cursor.close()
    connection.close()
if __name__ == "__main__":
    fetch_customers()