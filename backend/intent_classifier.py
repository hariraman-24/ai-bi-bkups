class IntentClassifier:

    def classify(self, question):

        q = question.lower()

        if "sales" in q or "customer" in q or "employee" in q:
            return "database"

        elif "revenue" in q or "finance" in q:
            return "finance"

        elif "csv" in q or "file" in q or "pdf" in q:
            return "file"

        else:
            return "unknown"