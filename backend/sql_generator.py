import requests
import re


class SQLGenerator:

    def generate_sql(self, question, schema_context=None, db_type="mysql"):

        q = question.lower().strip()

        # =====================================================
        # 💰 PROFIT / FINANCE
        # =====================================================
        if any(x in q for x in [
            "profit",
            "loss",
            "making money",
            "profitability",
            "are we making profit"
        ]):

            return """
            SELECT
                SUM(revenue) AS total_revenue,
                SUM(expenses) AS total_expenses,
                SUM(revenue) - SUM(expenses) AS total_profit
            FROM finance;
            """

        # =====================================================
        # 💰 REVENUE
        # =====================================================
        if "revenue" in q:

            if any(x in q for x in [
                "highest",
                "top",
                "maximum",
                "max"
            ]):

                return """
                SELECT *
                FROM finance
                ORDER BY revenue DESC
                LIMIT 1;
                """

            if any(x in q for x in [
                "lowest",
                "minimum",
                "min"
            ]):

                return """
                SELECT *
                FROM finance
                ORDER BY revenue ASC
                LIMIT 1;
                """

            return """
            SELECT
                department,
                revenue,
                expenses,
                (revenue - expenses) AS profit
            FROM finance
            ORDER BY revenue DESC;
            """

        # =====================================================
        # 🔝 HIGHEST SINGLE SALE
        # =====================================================
        if any(x in q for x in [
            "highest sale",
            "highest single sale",
            "largest sale",
            "max sale",
            "biggest sale"
        ]):

            return """
            SELECT
                s.sale_id,
                p.product_name,
                c.customer_name,
                e.employee_name,
                s.sales_amount,
                s.sale_date
            FROM sales s
            LEFT JOIN products p
                ON s.product_id = p.product_id
            LEFT JOIN customers c
                ON s.customer_id = c.customer_id
            LEFT JOIN employees e
                ON s.employee_id = e.employee_id
            ORDER BY s.sales_amount DESC
            LIMIT 1;
            """

        # =====================================================
        # 🔻 LOWEST SALE
        # =====================================================
        if any(x in q for x in [
            "lowest sale",
            "minimum sale",
            "smallest sale"
        ]):

            return """
            SELECT
                s.sale_id,
                p.product_name,
                c.customer_name,
                e.employee_name,
                s.sales_amount,
                s.sale_date
            FROM sales s
            LEFT JOIN products p
                ON s.product_id = p.product_id
            LEFT JOIN customers c
                ON s.customer_id = c.customer_id
            LEFT JOIN employees e
                ON s.employee_id = e.employee_id
            ORDER BY s.sales_amount ASC
            LIMIT 1;
            """

        # =====================================================
        # 📊 PRODUCT PRICE RANGE
        # =====================================================
        if any(x in q for x in [
            "price range",
            "product price range",
            "range of products",
            "range of price"
        ]):

            return """
            SELECT
                MIN(price) AS min_price,
                MAX(price) AS max_price,
                AVG(price) AS average_price
            FROM products;
            """

        # =====================================================
        # 📊 SALES RANGE
        # =====================================================
        if any(x in q for x in [
            "sales range",
            "range of sales"
        ]):

            return """
            SELECT
                MIN(sales_amount) AS min_sales,
                MAX(sales_amount) AS max_sales,
                AVG(sales_amount) AS average_sales
            FROM sales;
            """

        # =====================================================
        # 📊 TOTAL SALES
        # =====================================================
        if any(x in q for x in [
            "total sales",
            "how much sales",
            "sales did we make",
            "overall sales",
            "sales summary",
            "business revenue",
            "sales amount"
        ]):

            return """
            SELECT
                SUM(sales_amount) AS total_sales
            FROM sales;
            """

        # =====================================================
        # 📊 AVERAGE SALES
        # =====================================================
        if any(x in q for x in [
            "average sales",
            "avg sales",
            "mean sales"
        ]):

            return """
            SELECT
                AVG(sales_amount) AS average_sales
            FROM sales;
            """

        # =====================================================
        # 📊 SALES COUNT
        # =====================================================
        if any(x in q for x in [
            "how many sales",
            "count sales",
            "number of sales"
        ]):

            return """
            SELECT
                COUNT(*) AS total_sales_records
            FROM sales;
            """

        # =====================================================
        # 📦 PRODUCT PERFORMANCE
        # =====================================================
        if any(x in q for x in [
            "top product",
            "top products",
            "best selling product",
            "selling well",
            "product performance",
            "which product is selling well",
            "products by sales"
        ]):

            match = re.search(r"top\s+(\d+)", q)

            limit = int(match.group(1)) if match else 5

            return f"""
            SELECT
                p.product_name,
                p.category,
                SUM(s.sales_amount) AS total_sales
            FROM sales s
            JOIN products p
                ON s.product_id = p.product_id
            GROUP BY p.product_id, p.product_name, p.category
            ORDER BY total_sales DESC
            LIMIT {limit};
            """

        # =====================================================
        # 👨‍💼 EMPLOYEE PERFORMANCE
        # =====================================================
        if any(x in q for x in [
            "top employee",
            "best employee",
            "employee performance",
            "who is doing best",
            "employee wise sales"
        ]):

            match = re.search(r"top\s+(\d+)", q)

            limit = int(match.group(1)) if match else 5

            return f"""
            SELECT
                e.employee_name,
                e.department,
                SUM(s.sales_amount) AS total_sales
            FROM sales s
            JOIN employees e
                ON s.employee_id = e.employee_id
            GROUP BY e.employee_id, e.employee_name, e.department
            ORDER BY total_sales DESC
            LIMIT {limit};
            """

        # =====================================================
        # 👥 CUSTOMER PERFORMANCE
        # =====================================================
        if any(x in q for x in [
            "top customers",
            "best customers",
            "customer performance",
            "highest buying customer"
        ]):

            return """
            SELECT
                c.customer_name,
                c.region,
                SUM(s.sales_amount) AS total_purchase
            FROM sales s
            JOIN customers c
                ON s.customer_id = c.customer_id
            GROUP BY c.customer_id, c.customer_name, c.region
            ORDER BY total_purchase DESC
            LIMIT 10;
            """

        # =====================================================
        # 🌍 REGION WISE SALES
        # =====================================================
        if any(x in q for x in [
            "sales by region",
            "region wise sales",
            "customers by region",
            "customer region"
        ]):

            return """
            SELECT
                c.region,
                COUNT(DISTINCT c.customer_id) AS total_customers,
                SUM(s.sales_amount) AS total_sales
            FROM customers c
            LEFT JOIN sales s
                ON c.customer_id = s.customer_id
            GROUP BY c.region
            ORDER BY total_sales DESC;
            """

        # =====================================================
        # 📂 CATEGORY WISE SALES
        # =====================================================
        if any(x in q for x in [
            "sales by category",
            "category wise sales",
            "product category"
        ]):

            return """
            SELECT
                p.category,
                SUM(s.sales_amount) AS total_sales
            FROM sales s
            JOIN products p
                ON s.product_id = p.product_id
            GROUP BY p.category
            ORDER BY total_sales DESC;
            """

        # =====================================================
        # 🏢 DEPARTMENT PERFORMANCE
        # =====================================================
        if any(x in q for x in [
            "department performance",
            "sales by department",
            "best department"
        ]):

            return """
            SELECT
                e.department,
                SUM(s.sales_amount) AS total_sales
            FROM sales s
            JOIN employees e
                ON s.employee_id = e.employee_id
            GROUP BY e.department
            ORDER BY total_sales DESC;
            """

        # =====================================================
        # 📅 MONTH FILTER
        # =====================================================
        month_map = {
            "january": 1,
            "february": 2,
            "march": 3,
            "april": 4,
            "may": 5,
            "june": 6,
            "july": 7,
            "august": 8,
            "september": 9,
            "october": 10,
            "november": 11,
            "december": 12
        }

        found_months = [
            month_map[m]
            for m in month_map
            if m in q
        ]

        # MONTH RANGE
        if len(found_months) >= 2:

            start_month = min(found_months)
            end_month = max(found_months)

            return f"""
            SELECT
                sale_id,
                product_id,
                customer_id,
                employee_id,
                sales_amount,
                sale_date
            FROM sales
            WHERE MONTH(sale_date)
            BETWEEN {start_month} AND {end_month}
            ORDER BY sale_date;
            """

        # SINGLE MONTH
        if len(found_months) == 1:

            month_num = found_months[0]

            if "total" in q:

                return f"""
                SELECT
                    SUM(sales_amount) AS total_sales
                FROM sales
                WHERE MONTH(sale_date) = {month_num};
                """

            return f"""
            SELECT *
            FROM sales
            WHERE MONTH(sale_date) = {month_num}
            ORDER BY sale_date;
            """

        # =====================================================
        # 📈 SALES TREND
        # =====================================================
        if any(x in q for x in [
            "trend",
            "growth",
            "monthly",
            "business going",
            "how is business",
            "sales trend"
        ]):

            return """
            SELECT
                YEAR(sale_date) AS year,
                MONTH(sale_date) AS month,
                SUM(sales_amount) AS total_sales
            FROM sales
            GROUP BY YEAR(sale_date), MONTH(sale_date)
            ORDER BY year, month;
            """

        # =====================================================
        # 📅 DAILY SALES
        # =====================================================
        if any(x in q for x in [
            "daily sales",
            "sales by day",
            "day wise sales"
        ]):

            return """
            SELECT
                DATE(sale_date) AS sales_day,
                SUM(sales_amount) AS total_sales
            FROM sales
            GROUP BY DATE(sale_date)
            ORDER BY sales_day;
            """

        # =====================================================
        # 📅 YEAR FILTER
        # =====================================================
        year_match = re.search(r"(20\d{2})", q)

        if year_match:

            year = year_match.group(1)

            return f"""
            SELECT *
            FROM sales
            WHERE YEAR(sale_date) = {year}
            ORDER BY sale_date;
            """

        # =====================================================
        # 🔥 SHOW TABLE
        # =====================================================
        match = re.search(r"show\s+(\w+)", q)

        if match:

            table = match.group(1)

            allowed_tables = [
                "sales",
                "customers",
                "products",
                "employees",
                "finance"
            ]

            if table in allowed_tables:
                return f"SELECT * FROM {table};"

        # =====================================================
        # 🤖 SAFE AI FALLBACK
        # =====================================================
        if schema_context:
            schema = schema_context
        elif db_type.lower() == "postgresql":
            schema = """
finance(id, department, revenue, expenses)
"""
        else:
            schema = """
sales(sale_id, product_id, customer_id, employee_id, sales_amount, sale_date)
customers(customer_id, customer_name, region)
products(product_id, product_name, category, price)
employees(employee_id, employee_name, department)
finance(id, department, revenue, expenses)
"""

        prompt = f"""
You are a highly advanced AI Business Intelligence Assistant.
Generate ONLY a valid {db_type.upper()} SELECT query for the user's question.
If the question is completely unrelated to business, sales, finance, or the provided schema (e.g. sports, politics, "who won the world cup"), output exactly: "SELECT * FROM sales LIMIT 0;"

STRICT RULES:
1. ONLY use tables from schema.
2. ONLY SELECT queries.
3. NEVER use TOP keyword (use LIMIT instead).
4. NEVER use EXISTS, nested queries, subqueries, or MATCH() AGAINST().
5. If comparing or filtering by specific text names, use the IN clause (e.g. column IN ('name1', 'name2')) or LIKE.
6. If using aggregate functions (MAX, SUM), ALL other selected columns MUST be in a GROUP BY clause.
7. Output ONLY SQL code, no explanation, no markdown format.

Schema:
{schema}

Question:
{question}

SQL:
"""

        try:

            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "phi3",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )

            result = response.json().get("response", "")

            result = result.replace("```sql", "")
            result = result.replace("```", "")
            result = result.strip()

            match = re.search(
                r"(SELECT[\s\S]+?)(?:;|$)",
                result,
                re.IGNORECASE
            )

            if match:
                sql = match.group(1).strip() + ";"
            else:
                sql = result.strip()
                if not sql.endswith(";"):
                    sql += ";"

            blocked_words = [
                "delete",
                "drop",
                "truncate",
                "insert",
                "update",
                "alter",
                "exists",
                "top ",
                "union",
                "information_schema"
            ]

            if any(word in sql.lower() for word in blocked_words):
                return None

            if not sql.lower().startswith("select"):
                return None

            return sql

        except:
            pass

        # =====================================================
        # 🛡 SAFE FALLBACK
        # =====================================================
        if schema_context:
            return None
            
        if db_type.lower() == "postgresql":
            return "SELECT * FROM finance;"
            
        if "customer" in q:
            return "SELECT * FROM customers;"

        if "employee" in q:
            return "SELECT * FROM employees;"

        if "product" in q:
            return "SELECT * FROM products;"

        if "finance" in q:
            return "SELECT * FROM finance;"

        return "SELECT * FROM sales;"