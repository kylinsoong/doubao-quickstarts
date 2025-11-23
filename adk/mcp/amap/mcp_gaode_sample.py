# mcp_adk_client.py
# 使用 Google ADK 实现高德 MCP Client 的 ReAct + Function Calling

import os
from veadk import Agent, Runner
from google.adk.tools import FunctionTool
from google.genai import types
import asyncio



# === 1. 定义原始函数，用于调用高德地图 API（此处为 Stub，可替换为真实 HTTP 请求） ===
def maps_geo(name: str, region: str = "") -> dict:
    """
    Retrieves the geographical coordinates (latitude and longitude) of a given place name or Point of Interest (POI).

    This function is currently a stub and can be replaced with an actual HTTP request using libraries like requests or asynchttp to call the Amap Geo API.

    Args:
        name (str): The name of the place or POI for which the geographical coordinates are to be retrieved.
        region (str, optional): The region where the place or POI is located. This can help narrow down the search. Defaults to None.

    Returns:
        dict: A dictionary containing the geographical coordinates in the format {"location": "longitude,latitude"}. 
              In the stub implementation, it returns a hard - coded location.
    """
    # TODO: 用 requests/asynchttp 调用高德 Geo API
    print(f"[Stub] maps_geo(name={name}, region={region})")
    return {"location": "117.210813,39.14393"}


def maps_around_search(location: str, keyword: str, radius: int = 1000) -> dict:
    """
    Searches for a list of Points of Interest (POIs) of a specified type around a given set of geographical coordinates.

    This function simulates the process of searching for POIs around a given location within a specified radius.

    Args:
        location (str): The geographical coordinates (in the format "longitude,latitude") around which the search is to be performed.
        keyword (str): The type or keyword of the POIs to search for (e.g., "restaurant", "hotel").
        radius (int, optional): The radius (in meters) within which to search for the POIs. Defaults to 1000.

    Returns:
        dict: A dictionary containing a list of POIs. Each POI is represented as a dictionary with at least an "id" key.
    """
    print(f"[Stub] maps_around_search(location={location}, keyword={keyword}, radius={radius})")
    return {"pois": [{"id": f"B0FFF{idx}"} for idx in range(1, 4)]}


def maps_search_detail(poiid: str) -> dict:
    """
    Retrieves detailed information about a specific Point of Interest (POI) based on its unique identifier.

    This function simulates the process of fetching detailed information about a POI given its ID.

    Args:
        poiid (str): The unique identifier of the POI for which detailed information is to be retrieved.

    Returns:
        dict: A dictionary containing detailed information about the POI, such as its name, ID, and geographical coordinates.
    """
    print(f"[Stub] maps_search_detail(poiid={poiid})")
    return {"id": poiid, "name": f"五星酒店-{poiid[-1]}", "location": "117.211000,39.144000"}


def maps_distance(origins: str, destinations: str) -> dict:
    """
    Calculates the driving distance between two geographical locations.

    This function simulates the calculation of the driving distance between two given sets of geographical coordinates.

    Args:
        origins (str): The geographical coordinates (in the format "longitude,latitude") of the starting point.
        destinations (str): The geographical coordinates (in the format "longitude,latitude") of the destination point.

    Returns:
        dict: A dictionary containing the driving distance in meters between the two locations. In the stub implementation, 
              the distance is simulated based on the last digit of the destination coordinates.
    """
    print(f"[Stub] maps_distance(origins={origins}, destinations={destinations})")
    # 模拟距离
    return {"distance": 500 + int(destinations[-1]) * 100}

# === 2. 将原始函数包装成 ADK FunctionTool ===
maps_geo_tool = FunctionTool(
    func=maps_geo
)
maps_around_tool = FunctionTool(
    func=maps_around_search
)
maps_detail_tool = FunctionTool(
    func=maps_search_detail
)
maps_distance_tool = FunctionTool(
    func=maps_distance
)

# === 3. 创建 Agent 并注册工具 ===
agp_instruction = (
    "你是一个高德地图 MCP 客户端代理 (ADK Agent)，"
    "可以调用 maps_geo、maps_around_search、maps_search_detail、maps_distance 四个工具，"
    "帮助用户完成基于自然语言的地图查询与规划。"
)

agent = Agent(
    name="mcp_maps_agent",            # 或者其他支持 Function Calling 的模型
    description="高德地图 MCP Client 示例 Agent",
    instruction=agp_instruction,
    tools=[maps_geo_tool, maps_around_tool, maps_detail_tool, maps_distance_tool]
)




# Agent Interaction
runner = Runner(
    agent=agent
)


async def call_agent(query):
    """Calls the agent with the given query and prints the final response."""
    print(f"User query: {query}")
    response = await runner.run(
        messages=query
    )
    print(f"Agent response: {response}")


# === 4. 运行 Agent (CLI) ===
if __name__ == "__main__":
    asyncio.run(call_agent("明天去天津之眼附近，帮我规划五星级酒店，从和平大街过去有多远，安排一下周边4个小时逛街的攻略。"))



