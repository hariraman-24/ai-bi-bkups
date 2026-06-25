from intent_classifier import IntentClassifier


class QueryProcessor:

    def __init__(self):
        self.classifier = IntentClassifier()

    def process_question(self, question):

        intent = self.classifier.classify(question)

        if intent == "database":

            if "sales" in question.lower():
                return {"source": "mysql", "query": "SELECT * FROM sales"}

            elif "customer" in question.lower():
                return {"source": "mysql", "query": "SELECT * FROM customers"}

            elif "employee" in question.lower():
                return {"source": "mysql", "query": "SELECT * FROM employees"}

        elif intent == "finance":
            return {"source": "postgres", "query": "SELECT * FROM finance"}

        elif intent == "file":
            return {"source": "file", "path": "files/sample.csv"}

        else:
            return {"source": "none"}