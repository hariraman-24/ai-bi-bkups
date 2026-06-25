import requests

data = {
    "question": "read pdf file"
}

response = requests.post(
    "http://127.0.0.1:5000/query",
    json=data
)

print(response.json())