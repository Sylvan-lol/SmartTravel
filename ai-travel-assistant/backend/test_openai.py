from openai import OpenAI
from app.config import Config

# 初始化 OpenAI 客户端
client = OpenAI(
    api_key=Config.LLM_API_KEY,
    base_url=Config.LLM_BASE_URL
)

# 使用的模型
MODEL = Config.LLM_MODEL

# 测试基本对话
print("测试OpenAI API...")
try:
    # 调用 OpenAI API
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": "你好，我是一个旅行者，需要一些旅行建议。"}
        ],
        max_tokens=500,
        temperature=0.7
    )

    # 处理响应
    message = response.choices[0].message
    print("回复:", message.content)
except Exception as e:
    print("错误:", str(e))
