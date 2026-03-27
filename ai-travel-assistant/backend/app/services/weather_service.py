import httpx
import logging
from app.config import Config

logger = logging.getLogger(__name__)

async def get_weather(city: str) -> dict:
    """调用高德地图 API 获取当前天气"""
    try:
        async with httpx.AsyncClient() as client:
            url = "https://restapi.amap.com/v3/weather/weatherInfo"
            params = {
                "key": Config.AMAP_API_KEY,
                "city": city,
                "extensions": "base",  # base=实时天气，all=预报天气
                "output": "json"       # 返回格式
            }
            logger.info(f"Calling Gaode weather API: {url} with params: {params}")
            response = await client.get(url, params=params, timeout=10)
            logger.info(f"Weather API response status: {response.status_code}")
            
            # 检查响应状态码
            if response.status_code != 200:
                logger.error(f"Weather API returned non-200 status: {response.status_code}")
                return {"error": f"天气服务返回错误: {response.status_code}"}
            
            # 尝试解析 JSON
            try:
                data = response.json()
            except Exception as e:
                logger.error(f"Failed to parse weather API response: {e}")
                return {"error": f"天气服务返回无效数据: {str(e)}"}
            
            # 调用成功
            if data["status"] == "1":
                weather = data["lives"][0]
                result = {
                    "城市": weather["city"],
                    "天气": weather["weather"],
                    "温度": weather["temperature"] + "℃",
                    "风向": weather["winddirection"],
                    "湿度": weather["humidity"] + "%",
                    "发布时间": weather["reporttime"]
                }
                return result
            else:
                logger.error(f"Weather API returned error: {data['info']}")
                return {"错误": f"调用失败：{data['info']}"}
    except Exception as e:
        logger.error(f"Error in get_weather: {e}", exc_info=True)
        return {"错误": f"网络异常：{str(e)}"}
