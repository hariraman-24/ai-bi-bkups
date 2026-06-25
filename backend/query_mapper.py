class QueryMapper:

    def map_question_to_sql(self, question):

        q = question.lower()

        if "sales" in q:
            return "SELECT * FROM sales"

        elif "customer" in q:
            return "SELECT * FROM customers"

        elif "product" in q:
            return "SELECT * FROM products"

        elif "employee" in q:
            return "SELECT * FROM employees"

        elif "finance" in q or "revenue" in q:
            return "SELECT * FROM finance"

        else:
            return None