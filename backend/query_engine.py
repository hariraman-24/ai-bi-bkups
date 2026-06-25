from db_connection import connect_db
import pandas as pd


def run_query(sql_query):
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(sql_query)

    results = cursor.fetchall()

    df = pd.DataFrame(results)

    print("\nQuery Result:\n")
    print(df)

    cursor.close()
    connection.close()


if __name__ == "__main__":
    query = "SELECT * FROM employees"
    run_query(query)