import json
from openai import OpenAI
from app.config import Config
from app.services.weather_service import get_weather
from app.services.map_service import get_route

# 初始化 OpenAI 客户端
client = OpenAI(
    api_key=Config.LLM_API_KEY,
    base_url=Config.LLM_BASE_URL
)

# 使用的模型
MODEL = Config.LLM_MODEL

# 测试天气查询工具
async def test_weather_tool():
    print("测试天气查询工具...")
    try:
        result = await get_weather("北京")
        print(f"天气查询结果: {result}")
        return result
    except Exception as e:
        print(f"错误: {str(e)}")
        return None

# 测试路线规划工具
async def test_route_tool():
    print("测试路线规划工具...")
    try:
        # 使用北京天安门和故宫的经纬度
        result = await get_route("116.397428,39.90923", "116.407428,39.91923")
        print(f"路线规划结果: {result}")
        return result
    except Exception as e:
        print(f"错误: {str(e)}")
        return None

# 测试OpenAI工具调用
async def test_openai_tool_calls():
    print("测试OpenAI工具调用...")
    try:
        # 构建系统提示
        system_prompt = {
            "role": "system",
            "content": "你是一个智能旅行助手，能够帮助用户查询天气和规划路线。当用户询问天气时，使用query_weather工具，参数city为城市名称；当用户询问路线时，使用plan_route工具，参数origin和destination为经纬度坐标，格式为'经度,纬度'。请使用OpenAI标准的工具调用格式，不要使用其他格式。"
        }
        
        # 构建消息
        messages = [
            system_prompt,
            {"role": "user", "content": "北京的天气怎么样？"}
        ]
        
        # 构建工具描述
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "query_weather",
                    "description": "查询指定城市的实时天气，当用户询问某个城市的天气时使用",
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
        
        # 调用OpenAI API
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            max_tokens=65536,
            temperature=1.0
        )
        
        # 处理响应
        message = response.choices[0].message
        print(f"AI响应: {message}")
        
        # 如果有工具调用
        if message.tool_calls:
            print("AI调用了工具")
            tool_call = message.tool_calls[0]
            print(f"工具名称: {tool_call.function.name}")
            print(f"工具参数: {tool_call.function.arguments}")
            
            # 执行工具调用
            if tool_call.function.name == "query_weather":
                args = json.loads(tool_call.function.arguments)
                weather_result = await get_weather(args["city"])
                print(f"工具执行结果: {weather_result}")
                
                # 构建工具结果消息
                tool_result_message = {
                    "role": "tool",
                    "content": json.dumps(weather_result),
                    "tool_call_id": tool_call.id
                }
                
                # 再次调用AI，获取最终回复
                final_messages = messages + [
                    {"role": "assistant", "content": message.content, "tool_calls": [{
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments
                        }
                    }]},
                    tool_result_message
                ]
                
                final_response = client.chat.completions.create(
                    model=MODEL,
                    messages=final_messages,
                    max_tokens=65536,
                    temperature=1.0
                )
                
                final_message = final_response.choices[0].message
                print(f"最终回复: {final_message.content}")
                return final_message.content
        else:
            print("AI没有调用工具")
            return message.content
    except Exception as e:
        print(f"错误: {str(e)}")
        return None

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_weather_tool())
    asyncio.run(test_route_tool())
    asyncio.run(test_openai_tool_calls())
