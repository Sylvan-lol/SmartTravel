import requests
import json

print("测试聊天接口...")

# 测试天气查询
url = "http://localhost:8080/api/chat"
headers = {"Content-Type": "application/json"}
data = {
    "messages": [
        {"role": "user", "content": "北京的天气怎么样？"}
    ],
    "user_id": "default"
}

response = requests.post(url, headers=headers, data=json.dumps(data))

print(f"状态码: {response.status_code}")
print(f"响应: {response.json()}")