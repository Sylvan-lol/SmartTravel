import requests

url = 'http://localhost:8080/api/chat'
headers = {'Content-Type': 'application/json'}
data = {
    'messages': [
        {'role': 'user', 'content': '北京的天气怎么样？'}
    ]
}

response = requests.post(url, headers=headers, json=data)
print(f"Status code: {response.status_code}")
print(f"Response: {response.json()}")