rom mcp.server.fastmcp import FastMCP
import asyncio

mcp = FastMCP(name="weather-demo", host="0.0.0.0", port=1234)

@mcp.tool(name="get_weather", description="获取指定城市的天气信息")
async def get_weather(city: str) -> str:
    """
    获取指定城市的天气信息
    """
    weather_data = {
        "北京": "北京：晴，25°C",
        "上海": "上海：多云，27°C"
    }
    return weather_data.get(city, f"{city}：天气信息未知")

@mcp.tool(name="suggest_activity", description="根据天气描述推荐适合的活动")
async def suggest_activity(condition: str) -> str:
    """
    根据天气描述推荐适合的活动
    """
    if "晴" in condition:
        return "天气晴朗，推荐你去户外散步或运动。"
    elif "多云" in condition:
        return "多云天气适合逛公园或咖啡馆。"
    elif "雨" in condition:
        return "下雨了，建议你在家阅读或看电影。"
    else:
        return "建议进行室内活动。"
