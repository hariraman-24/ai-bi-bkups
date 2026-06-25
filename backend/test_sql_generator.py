from sql_generator import SQLGenerator
from db_connection import connect_db
from query_validator import QueryValidator

generator = SQLGenerator()
validator = QueryValidator()

question = "show customers from the east region"

sql_query = generator.generate_sql(question)

print("Generated SQL:", sql_query)
# VALIDATE
if not validator.validate(sql_query):
    print("Query blocked for security reasons")
    exit()

connection = connect_db()
cursor = connection.cursor()

cursor.execute(sql_query)

results = cursor.fetchall()

for row in results:
    print(row)

cursor.close()
connection.close()