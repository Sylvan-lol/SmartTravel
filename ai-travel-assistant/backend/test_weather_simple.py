import requests

print("测试天气查询功能...")
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
    result = response.json()
    print(f"回复: {result['message']}")
except Exception as e:
    print(f"错误: {str(e)}")
