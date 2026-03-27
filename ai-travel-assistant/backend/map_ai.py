import requests


# ===================== 已自动填入你的高德Web服务Key =====================
GAODE_KEY = "816307678b20f6842a8dbcbd80faa20f"
# ======================================================================


# ------------------- 1. 获取实时天气 -------------------
def get_gaode_weather(city="北京"):

    url = "https://restapi.amap.com/v3/weather/weatherInfo"
    params = {
        "key": GAODE_KEY,
        "city": city,
        "extensions": "base",
        "output": "json"
    }
    try:

        res = requests.get(url, params=params, timeout=10)
        data = res.json()

        if data["status"] == "1":

            w = data["lives"][0]

            return f"【{w['city']}】实时天气：{w['weather']}，温度{w['temperature']}℃，湿度{w['humidity']}%"

        return f"天气查询失败：{data['info']}"

    except Exception as e:

        return f"网络错误：{str(e)}"


# ------------------- 2. 获取驾车导航路线 -------------------
def get_gaode_navigation(origin="116.481028,39.921983", destination="116.397428,39.90923"):

    url = "https://restapi.amap.com/v3/direction/driving"
    params = {
        "key": GAODE_KEY,
        "origin": origin,
        "destination": destination,
        "output": "json"
    }
    try:

        res = requests.get(url, params=params, timeout=10)
        data = res.json()

        if data["status"] == "1":

            route = data["route"]["paths"][0]

            return f"导航路线：全程{round(int(route['distance'])/1000,1)}公里，预计耗时{round(int(route['duration'])/60,1)}分钟"

        return f"导航查询失败：{data['info']}"

    except Exception as e:

        return f"网络错误：{str(e)}"


# ------------------- 3. AI Agent 接入（直接喂给AI） -------------------
def ai_agent_prompt():

    # 获取数据
    weather_info = get_gaode_weather()
    nav_info = get_gaode_navigation()

    # 拼接成AI可理解的prompt
    prompt = f"""
    你是智能助手，根据以下信息回答用户：
    1. {weather_info}
    2. {nav_info}
    请用自然语言简洁回复。
    """

    return prompt


# ------------------- 一键运行 -------------------
if __name__ == "__main__":

    print("="*50)
    print("📊 高德天气结果：")
    print(get_gaode_weather())
    print("\n🧭 高德导航结果：")
    print(get_gaode_navigation())
    print("\n🤖 AI Agent 专用Prompt：")
    print(ai_agent_prompt())
    print("="*50)