import asyncio
from app.services.weather_service import get_weather
from app.services.map_service import get_route

async def test_services():
    """测试天气和地图服务"""
    print("测试天气服务...")
    weather_result = await get_weather("北京")
    print(f"天气服务结果: {weather_result}")
    
    print("\n测试地图服务...")
    route_result = await get_route("116.481028,39.921983", "116.397428,39.90923")
    print(f"地图服务结果: {route_result}")
    
    print("\n服务测试完成！")

if __name__ == "__main__":
    asyncio.run(test_services())