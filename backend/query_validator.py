import re


class QueryValidator:

    def validate(self, sql):

        if not sql:
            return False

        sql_clean = sql.lower().strip()

        # ==============================
        # ✅ ONLY SELECT ALLOWED
        # ==============================
        if not sql_clean.startswith("select"):
            return False

        # ==============================
        # ❌ BLOCK MULTIPLE QUERIES
        # ==============================
        if ";" in sql_clean[:-1]:   # allow only ending semicolon
            return False

        # ==============================
        # ❌ BLOCK DANGEROUS KEYWORDS
        # ==============================
        blocked_keywords = [
            "drop", "delete", "update", "insert", "truncate",
            "alter", "create", "replace", "grant", "revoke"
        ]

        for word in blocked_keywords:
            if re.search(rf"\b{word}\b", sql_clean):
                return False

        # ==============================
        # ❌ BLOCK SQL INJECTION PATTERNS
        # ==============================
        injection_patterns = [
            r"--",            # inline comments
            r"/\*",           # block comment start
            r"\*/",           # block comment end
            r"union\s+select",
            r"or\s+1=1",
            r"or\s+'1'='1'",
            r"xp_",           # SQL Server injection
        ]

        for pattern in injection_patterns:
            if re.search(pattern, sql_clean):
                return False

        # ==============================
        # ✅ ALLOWED TABLES ONLY
        # ==============================
        allowed_tables = ["sales", "customers", "products", "employees", "finance"]

        table_found = any(tbl in sql_clean for tbl in allowed_tables)

        if not table_found:
            return False

        # ==============================
        # ⚠️ OPTIONAL: LIMIT PROTECTION
        # ==============================
        if "limit" not in sql_clean and "group by" not in sql_clean:
            # prevent huge data dump
            return False

        return True