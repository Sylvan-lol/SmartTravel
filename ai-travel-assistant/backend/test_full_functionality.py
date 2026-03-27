import requests
import json

print("测试完整功能...")

# 测试天气查询
def test_weather():
    print("\n测试天气查询功能...")
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
        return result
    except Exception as e:
        print(f"错误: {str(e)}")
        return None

# 测试路线规划
def test_route():
    print("\n测试路线规划功能...")
    try:
        response = requests.post(
            "http://localhost:8002/api/chat",
            json={
                "messages": [
                    {"role": "user", "content": "从北京天安门到故宫的驾车路线"}
                ],
                "user_id": "default"
            }
        )
        print(f"状态码: {response.status_code}")
        result = response.json()
        print(f"回复: {result['message']}")
        if 'map_data' in result and result['map_data']:
            print("地图数据: 已获取")
        return result
    except Exception as e:
        print(f"错误: {str(e)}")
        return None

# 测试AI对话
def test_ai_chat():
    print("\n测试AI对话功能...")
    try:
        response = requests.post(
            "http://localhost:8002/api/chat",
            json={
                "messages": [
                    {"role": "user", "content": "我计划去北京旅游，有什么推荐的景点？"}
                ],
                "user_id": "default"
            }
        )
        print(f"状态码: {response.status_code}")
        result = response.json()
        print(f"回复: {result['message']}")
        return result
    except Exception as e:
        print(f"错误: {str(e)}")
        return None

if __name__ == "__main__":
    # 先启动后端服务
    import subprocess
    import time
    import os
    
    # 启动后端服务
    print("启动后端服务...")
    server_process = subprocess.Popen(
        ["python", "run.py"],
        cwd=os.path.dirname(os.path.abspath(__file__)),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # 等待服务启动
    time.sleep(5)
    
    try:
        # 测试功能
        test_weather()
        test_route()
        test_ai_chat()
    finally:
        # 停止后端服务
        print("\n停止后端服务...")
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()
