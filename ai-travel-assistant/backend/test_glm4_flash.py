from zai import ZhipuAiClient
from app.config import Config

# 初始化客户端
client = ZhipuAiClient(api_key=Config.ZHIPU_API_KEY)

# 测试基本对话
print("测试智谱AI GLM-4-Flash模型...")
try:
    response = client.chat.completions.create(
        model="glm-4-flash",
        messages=[
            {"role": "user", "content": "你好，我是一个旅行者，需要一些旅行建议。"}
        ],
        max_tokens=500,
        temperature=0.7
    )
    print("回复:", response.choices[0].message.content)
except Exception as e:
    print("错误:", str(e))
