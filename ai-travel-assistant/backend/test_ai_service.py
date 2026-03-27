import asyncio
from app.services.ai_service import chat_with_ai

async def test_chat():
    print("测试AI服务...")
    messages = [
        {"role": "user", "content": "北京的天气怎么样？"}
    ]
    result = await chat_with_ai(messages)
    print("回复:", result["content"])
    print("地图数据:", result["map_data"])

if __name__ == "__main__":
    asyncio.run(test_chat())
