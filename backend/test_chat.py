import requests

url = "http://127.0.0.1:5000/query"

while True:

    question = input("Ask question: ")

    if question.lower() == "exit":
        break

    response = requests.post(url, json={"question": question})

    print("\nResponse:")
    print(response.json())