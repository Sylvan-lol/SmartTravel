import requests

# 测试导航功能
def test_navigation():
    url = "http://localhost:8080/api/chat"
    data = {
        "messages": [
            {
                "role": "user",
                "content": "佛山到惠州坐高铁怎么做"
            }
        ]
    }
    
    response = requests.post(url, json=data)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    test_navigation()
