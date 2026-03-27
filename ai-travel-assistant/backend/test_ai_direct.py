import json
from zai import ZhipuAiClient
from app.config import Config

# 初始化智谱 AI 客户端
client = ZhipuAiClient(api_key=Config.ZHIPU_API_KEY)

# 测试基本对话
print("测试智谱AI GLM-4-Flash-250414模型...")
try:
    # 构建工具描述
    tools = [
        {
            "type": "function",
            "function": {
                "name": "query_weather",
                "description": "查询指定城市的实时天气",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "城市名称，例如：北京、上海"
                        }
                    },
                    "required": ["city"]
                }
            }
        }
    ]

    # 调用智谱 AI API
    response = client.chat.completions.create(
        model="GLM-4-Flash-250414",
        messages=[
            {"role": "user", "content": "北京的天气怎么样？"}
        ],
        tools=tools,
        tool_choice="auto",
        max_tokens=65536,
        temperature=1.0
    )

    # 处理响应
    message = response.choices[0].message
    print("回复:", message.content)
    if message.tool_calls:
        print("工具调用:", message.tool_calls)
except Exception as e:
    print("错误:", str(e))
