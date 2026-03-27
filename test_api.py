import requests
import json

# 测试从黄山到惠州的高铁查询
url = "http://localhost:8082/api/chat"
headers = {"Content-Type": "application/json"}

# 测试1：从黄山到惠州坐高铁
print("测试1：从黄山到惠州坐高铁")
data1 = {
    "messages": [
        {"role": "user", "content": "从黄山到惠州坐高铁可以怎么坐？给我详细信息"}
    ]
}

response1 = requests.post(url, headers=headers, data=json.dumps(data1))
print("Response status code:", response1.status_code)
print("Response content:", response1.text)

# 测试2：从北京到上海怎么走
print("\n测试2：从北京到上海怎么走")
data2 = {
    "messages": [
        {"role": "user", "content": "从北京到上海怎么走？"}
    ]
}

response2 = requests.post(url, headers=headers, data=json.dumps(data2))
print("Response status code:", response2.status_code)
print("Response content:", response2.text)

# 测试3：北京天气查询
print("\n测试3：北京天气查询")
data3 = {
    "messages": [
        {"role": "user", "content": "今天北京的天气如何？"}
    ]
}

response3 = requests.post(url, headers=headers, data=json.dumps(data3))
print("Response status code:", response3.status_code)
print("Response content:", response3.text)

# 测试4：RAG系统测试
print("\n测试4：RAG系统测试")
data4 = {
    "messages": [
        {"role": "user", "content": "黄山有哪些著名景点？"}
    ]
}

response4 = requests.post(url, headers=headers, data=json.dumps(data4))
print("Response status code:", response4.status_code)
print("Response content:", response4.text)

# 测试5：从广州到深圳坐高铁
print("\n测试5：从广州到深圳坐高铁")
data5 = {
    "messages": [
        {"role": "user", "content": "从广州到深圳坐高铁可以怎么坐？"}
    ]
}

response5 = requests.post(url, headers=headers, data=json.dumps(data5))
print("Response status code:", response5.status_code)
print("Response content:", response5.text)
