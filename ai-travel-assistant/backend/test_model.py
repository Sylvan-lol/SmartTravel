import requests

print("测试后端服务和GLM-4-Flash-250414模型...")
try:
    response = requests.post(
        "http://localhost:8002/api/chat",
        json={
            "messages": [
                {"role": "user", "content": "北京的天气怎么样？"}
            ],
            "user_id": "default"
        }
    )
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
except Exception as e:
    print(f"错误: {str(e)}")
