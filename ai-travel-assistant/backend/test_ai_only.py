from zai import ZhipuAiClient
from app.config import Config

# 初始化智谱 AI 客户端
client = ZhipuAiClient(
    api_key=Config.ZHIPU_API_KEY,
    base_url="https://open.bigmodel.cn/api/paas/v4"
)

# 测试基本对话
print("测试智谱AI GLM-4-Flash-250414模型...")
try:
    # 调用智谱 AI API
    response = client.chat.completions.create(
        model="GLM-4-Flash-250414",
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
