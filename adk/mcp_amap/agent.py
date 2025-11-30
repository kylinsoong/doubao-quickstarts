import asyncio
from dotenv import load_dotenv
import os
from google.genai import types
from veadk.agent import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService # Optional
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters, StdioConnectionParams, SseConnectionParams, StreamableHTTPConnectionParams

from google.adk.agents.run_config import RunConfig, StreamingMode
# SSE Streaming
sse_config = RunConfig(
    streaming_mode=StreamingMode.SSE
)

# No Streaming (blocking)
blocking_config = RunConfig(
    streaming_mode=StreamingMode.NONE
)

load_dotenv()
GAODE_API_KEY = os.getenv('GAODE_API_KEY')

mode = "sse"

def build_mcptoolset(mode):
    print("Attempting to connect to MCP amap Maps server...")
    mcp_toolset = None
    if mode == 'sse':
        # 使用SSE连接方式
        # 注意：这里需要实际的SSE URL，高德地图MCP服务器可能不提供SSE端点
        # 这只是一个示例，您需要根据实际的MCP服务器配置进行调整
        print("Using SSE connection...")
        mcp_toolset = MCPToolset(
            connection_params=SseConnectionParams(
                url="https://mcp.amap.com/sse?key=" + GAODE_API_KEY,  
                timeout=30.0,
                sse_read_timeout=300.0
            )
        )
    elif mode == 'stdio':
        print("Using Stdio connection...")
        # 创建MCP服务器参数
        server_params = StdioServerParameters(
            command="npx",
            args=["-y", "@amap/amap-maps-mcp-server"],
            # 设置环境变量
            env={
                "AMAP_MAPS_API_KEY": GAODE_API_KEY
            }
        )
        
        # 创建MCPToolset实例
        mcp_toolset = MCPToolset(
            connection_params=StdioConnectionParams(
                server_params=server_params,
            )
        )
    elif mode == 'streamable_http':
        # 使用Streamable HTTP连接方式
        # 注意：这里需要实际的HTTP URL，高德地图MCP服务器可能不提供HTTP端点
        # 这只是一个示例，您需要根据实际的MCP服务器配置进行调整
        print("Using Streamable HTTP connection...")
        mcp_toolset = MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url="https://mcp.amap.com/mcp?key=" + GAODE_API_KEY,  
                timeout=30.0,
                http_read_timeout=300.0
            )
        )
    return mcp_toolset
            
def create_agent(mode):
    """创建根代理"""
    return Agent(
        name="gaode_assistant",
        instruction="""你是一个使用高德地图API的助手。你可以帮助用户：
        1. 搜索地点
        2. 获取路线规划
        3. 查询天气情况
        4. 其他与地图相关的服务
        
        请使用可用的工具来回答用户的问题，并提供有用的信息。
        """,
        description="一个使用高德地图API的助手",
        tools=[build_mcptoolset(mode)]  # 直接使用获取的工具列表
    )

root_agent = create_agent("stdio")