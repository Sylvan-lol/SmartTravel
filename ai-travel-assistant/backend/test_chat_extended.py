import requests
import json

# 测试天气查询
print("测试天气查询...")
url = "http://localhost:8080/api/chat"
headers = {"Content-Type": "application/json"}
data = {
    "messages": [
        {"role": "user", "content": "今天北京的天气如何？"}
    ],
    "user_id": "default"
}
response = requests.post(url, headers=headers, data=json.dumps(data))
print(f"状态码: {response.status_code}")
print(f"响应: {response.json()}")

# 测试旅游推荐
print("\n测试旅游推荐...")
data = {
    "messages": [
        {"role": "user", "content": "你推荐我去什么地方玩？"}
    ],
    "user_id": "default"
}
response = requests.post(url, headers=headers, data=json.dumps(data))
print(f"状态码: {response.status_code}")
print(f"响应: {response.json()}")

# 测试交通查询
print("\n测试交通查询...")
data = {
    "messages": [
        {"role": "user", "content": "从佛山到广州交通"}
    ],
    "user_id": "default"
}
response = requests.post(url, headers=headers, data=json.dumps(data))
print(f"状态码: {response.status_code}")
print(f"响应: {response.json()}")