import psycopg2

def connect_postgres():
    connection = psycopg2.connect(
        host="localhost",
        database="finance_db",
        user="postgres",
        password="IncorrecT2410__2005"
    )
    
    return connection


if __name__ == "__main__":
    conn = connect_postgres()
    print("Connected to PostgreSQL successfully")
    conn.close()