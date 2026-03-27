import requests

print("测试后端服务健康状态...")
response = requests.get("http://localhost:8080/api/health")
print(f"状态码: {response.status_code}")
print(f"响应: {response.json()}")

print("\n测试天气查询...")
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