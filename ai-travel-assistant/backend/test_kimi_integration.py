import asyncio
from app.services.ai_service import chat_with_ai

async def test_kimi_integration():
    """测试Kimi模型集成"""
    print("测试Kimi模型集成...")
    
    # 测试天气查询
    print("\n测试1: 天气查询")
    messages = [
        {"role": "user", "content": "北京的天气怎么样？"}
    ]
    result = await chat_with_ai(messages)
    print(f"回复: {result['content']}")
    print(f"地图数据: {result['map_data']}")
    
    # 测试路线规划
    print("\n测试2: 路线规划")
    messages = [
        {"role": "user", "content": "从北京到上海的路线"}
    ]
    result = await chat_with_ai(messages)
    print(f"回复: {result['content']}")
    print(f"地图数据: {result['map_data']}")
    
    # 测试旅游推荐
    print("\n测试3: 旅游推荐")
    messages = [
        {"role": "user", "content": "推荐一些旅游景点"}
    ]
    result = await chat_with_ai(messages)
    print(f"回复: {result['content']}")
    print(f"地图数据: {result['map_data']}")
    
    # 测试普通对话
    print("\n测试4: 普通对话")
    messages = [
        {"role": "user", "content": "你好，你是谁？"}
    ]
    result = await chat_with_ai(messages)
    print(f"回复: {result['content']}")
    print(f"地图数据: {result['map_data']}")
    
    print("\n测试完成！")

if __name__ == "__main__":
    asyncio.run(test_kimi_integration())