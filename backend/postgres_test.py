from postgres_connection import connect_postgres
connection = connect_postgres()

cursor = connection.cursor()
cursor.execute("SELECT * FROM finance")
rows = cursor.fetchall()

print("Finance Table Data:\n")
for row in rows:
    print(row)
cursor.close()
connection.close()