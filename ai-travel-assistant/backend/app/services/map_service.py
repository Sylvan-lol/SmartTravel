import httpx
import logging
from app.config import Config

logger = logging.getLogger(__name__)

async def get_route(origin: str, destination: str) -> dict:
    """调用高德地图路径规划 API，返回路线数据（用于前端地图渲染）"""
    try:
        async with httpx.AsyncClient() as client:
            url = "your url like: https://restapi.amap.com/v3/direction/driving"
            params = {
                "key": Config.AMAP_API_KEY,
                "origin": origin,
                "destination": destination,
                "extensions": "all",  # 返回详细信息
                "output": "JSON"
            }
            logger.info(f"Calling Gaode navigation API: {url} with params: {params}")
            resp = await client.get(url, params=params, timeout=10.0)
            logger.info(f"Navigation API response status: {resp.status_code}")
            data = resp.json()
            
            if data["status"] != "1":
                logger.error(f"Navigation API returned error: {data.get('info', '路线规划失败')}")
                return {"error": data.get("info", "路线规划失败")}

            # 提取关键数据
            if "route" not in data or "paths" not in data["route"] or len(data["route"]["paths"]) == 0:
                logger.error(f"Route data not found in response: {data}")
                return {"error": "路线数据获取失败"}
            
            route = data["route"]["paths"][0]
            logger.info(f"Route data: {route}")
            # 检查必需字段（只要求 duration 和 distance）
            missing_fields = []
            if "duration" not in route:
                missing_fields.append("duration")
            if "distance" not in route:
                missing_fields.append("distance")
            
            if missing_fields:
                logger.error(f"Route data incomplete, missing fields: {missing_fields}")
                return {"error": f"路线数据不完整，缺少字段: {missing_fields}"}
            
            # 可选字段
            steps = route.get("steps", [])
            polyline = route.get("polyline", "")
            duration = int(route["duration"]) // 60  # 分钟
            distance = float(route["distance"]) / 1000  # 公里

            # 解析起点终点坐标（用于地图定位）
            origin_coords = origin.split(",")
            destination_coords = destination.split(",")

            return {
                "origin": {"lng": float(origin_coords[0]), "lat": float(origin_coords[1])},
                "destination": {"lng": float(destination_coords[0]), "lat": float(destination_coords[1])},
                "polyline": polyline,
                "distance_km": distance,
                "duration_min": duration,
                "steps": [{"instruction": step["instruction"], "distance": step["distance"]} for step in steps[:5]]  # 前5个步骤
            }
    except Exception as e:
        logger.error(f"Error in get_route: {e}", exc_info=True)
        return {"error": f"路线规划失败: {str(e)}"}
