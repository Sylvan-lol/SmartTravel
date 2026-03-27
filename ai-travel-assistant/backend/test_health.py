import requests

print("测试后端服务健康检查...")
try:
    response = requests.get("http://localhost:8001/api/health")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
except Exception as e:
    print(f"错误: {str(e)}")
