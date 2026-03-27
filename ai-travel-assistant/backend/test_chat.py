import requests

print("测试聊天接口...")

# 测试天气查询
response = requests.post(
    "http://localhost:8080/api/chat",
    json={
        "messages": [
            {"role": "user", "content": "北京的天气怎么样？"}
        ],
        "user_id": "default"
    }
)

print(f"状态码: {response.status_code}")
print(f"响应: {response.json()}")