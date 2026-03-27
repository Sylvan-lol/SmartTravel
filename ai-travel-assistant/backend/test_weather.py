import requests
import time
import subprocess
import os

print("测试天气查询功能...")

# 启动后端服务
print("启动后端服务...")
server_process = subprocess.Popen(
    ["python", "run.py"],
    cwd=os.path.dirname(os.path.abspath(__file__)),
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

# 等待服务启动
time.sleep(3)

try:
    # 测试天气查询
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
finally:
    # 停止后端服务
    print("\n停止后端服务...")
    server_process.terminate()
    try:
        server_process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        server_process.kill()
