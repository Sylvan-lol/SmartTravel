import asyncio
from app.services.ai_service import chat_with_ai

async def test_full_system():
    """测试完整系统功能"""
    print("测试完整系统功能...")
    
    # 测试天气查询 - 应该返回真实天气数据
    print("\n测试1: 天气查询")
    messages = [
        {"role": "user", "content": "北京的天气怎么样？"}
    ]
    result = await chat_with_ai(messages)
    print(f"回复: {result['content']}")
    print(f"地图数据: {result['map_data']}")
    
    # 测试路线规划 - 应该返回真实路线数据
    print("\n测试2: 路线规划")
    messages = [
        {"role": "user", "content": "从北京到上海的路线"}
    ]
    result = await chat_with_ai(messages)
    print(f"回复: {result['content']}")
    print(f"地图数据: {result['map_data']}")
    
    # 测试旅游推荐 - 应该返回推荐信息
    print("\n测试3: 旅游推荐")
    messages = [
        {"role": "user", "content": "推荐一些旅游景点"}
    ]
    result = await chat_with_ai(messages)
    print(f"回复: {result['content']}")
    print(f"地图数据: {result['map_data']}")
    
    # 测试普通对话 - 应该返回默认回复
    print("\n测试4: 普通对话")
    messages = [
        {"role": "user", "content": "你好，你是谁？"}
    ]
    result = await chat_with_ai(messages)
    print(f"回复: {result['content']}")
    print(f"地图数据: {result['map_data']}")
    
    print("\n系统测试完成！")

if __name__ == "__main__":
    asyncio.run(test_full_system())