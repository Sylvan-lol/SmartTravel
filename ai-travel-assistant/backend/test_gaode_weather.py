import asyncio
from app.services.weather_service import get_weather

async def test_weather():
    print("测试高德地图天气 API...")
    result = await get_weather("北京")
    print("天气查询结果:")
    print(result)

if __name__ == "__main__":
    asyncio.run(test_weather())