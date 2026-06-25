import requests
import json

class LLMEngine:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model = "phi3"

    def ask_llm(self, question):
        data = {
            "model": self.model,
            "prompt": f"Classify this question into one word: sales, finance, file, customer, product.\nQuestion: {question}",
            "stream": False
        }
        try:
            response = requests.post(self.url, json=data, timeout=5)
            result = response.json().get("response", "")
            return result.lower()
        except:
            return "general"

    def is_business_query_llm(self, question):
        prompt = f"""
        Determine if the following question is related to Business Intelligence, Sales, Finance, Company Data, or Data Analysis.
        Respond ONLY with 'YES' if it is a valid business/data question.
        Respond ONLY with 'NO' if it is an out-of-context question (like sports, politics, general trivia, e.g., 'who is the pm', 'who won worldcup').
        
        Question: {question}
        """
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        try:
            response = requests.post(self.url, json=data, timeout=5)
            result = response.json().get("response", "").strip().upper()
            if "YES" in result:
                return True
            if "NO" in result:
                return False
            return True # fallback safe
        except:
            return True # fallback safe

    def generate_chat_insight(self, question, data_str):
        prompt = f"""
        You are a highly professional Business Intelligence AI Assistant. Act like a mini ChatGPT tailored for data analytics.
        Provide deep, actionable, and highly accurate business insights based on the provided data to answer the user's question. Focus on trends, anomalies, and key takeaways.
        If the user asks to compare items, explicitly calculate and state the exact differences between them for absolute clarity.
        Do NOT mention that you are an AI or open-source model.
        Keep it to 2-3 sentences max.
        
        Question: {question}
        Data: {data_str}
        
        Professional AI Insight:
        """
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        try:
            response = requests.post(self.url, json=data, timeout=60)
            return response.json().get("response", "").strip()
        except Exception as e:
            print(f"LLM Insight Error: {e}")
            return "I apologize, but the AI is currently under high load and could not generate an analysis in time. Please try again in a moment."

    def answer_document_question(self, question, document_text):
        prompt = f"""
        You are a highly intelligent AI Assistant.
        Answer the user's question based strictly on the provided document text.
        If the answer is not in the text, say "I could not find the answer in the document."
        
        Document Text:
        {document_text}
        
        Question:
        {question}
        
        Answer (Keep it under 3 sentences):
        """
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 200
            }
        }
        try:
            response = requests.post(self.url, json=data, timeout=300)
            return response.json().get("response", "").strip()
        except Exception as e:
            print(f"LLM Document Error: {e}")
            return "I apologize, but the AI took too long to read this document. Local AI models require significant processing power for documents."

    def general_chat(self, question):
        prompt = f"""
        You are a highly intelligent and helpful AI Assistant, acting like ChatGPT.
        Answer the user's question perfectly, accurately, and comprehensively.
        You have deep knowledge about business, technology, science, and general topics.
        
        Question: {question}
        
        Answer:
        """
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        try:
            response = requests.post(self.url, json=data, timeout=120)
            return response.json().get("response", "").strip()
        except Exception as e:
            print(f"LLM General Chat Error: {e}")
            return "I apologize, but I am currently unable to connect to my AI brain. Please ensure Ollama is running."