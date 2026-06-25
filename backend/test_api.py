import requests

url = "http://127.0.0.1:5000/query"

question = input("Enter your question: ")

data = {"question": question}

response = requests.post(url, json=data)

print("\nResponse from MCP Server:")
print(response.json())