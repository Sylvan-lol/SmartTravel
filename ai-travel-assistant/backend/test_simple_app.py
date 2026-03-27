import requests

print("测试简单FastAPI应用...")
try:
    response = requests.get("http://localhost:8003/api/health")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
except Exception as e:
    print(f"错误: {str(e)}")
