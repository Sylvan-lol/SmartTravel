import asyncio
from app.services.map_service import get_route

async def test_navigation():
    print("测试高德地图导航 API...")
    # 北京天安门到北京西站的经纬度
    origin = "116.481028,39.921983"
    destination = "116.397428,39.90923"
    result = await get_route(origin, destination)
    print("导航查询结果:")
    print(result)

if __name__ == "__main__":
    asyncio.run(test_navigation())