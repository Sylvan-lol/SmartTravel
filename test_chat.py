import requests
import json

# 测试聊天接口
url = "http://localhost:8000/api/chat"
headers = {"Content-Type": "application/json"}
data = {
    "messages": [
        {
            "role": "user",
            "content": "你好，我是测试用户"
        }
    ],
    "user_id": "default"
}

print("发送请求...")
try:
    response = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
except Exception as e:
    print(f"请求失败: {str(e)}")
