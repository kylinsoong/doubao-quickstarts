# Reference : https://raphaelmansuy.github.io/adk_training/docs/mcp_integration
# SseConnectionParams（SSE）：作为 “单向推送专家”，SseConnectionParams（SSE）最适合用于实时性需求场景，
# 例如实时通知的下发、日志流的持续传输，以及监控数据的动态推送，能高效实现信息从服务端到客户端的单向实时传递。
# StdioServerParameters（Stdio）StdioServerParameters（Stdio）堪称 “本地双向通信王者”，
# 其核心优势在于本地环境下的双向数据交互，因此最适合应用于命令行工具的指令交互、桌面应用的本地数据传输，以及本地开发过程中的调试与通信需求。
# Streamable HTTP 有着 “标准化全能选手” 的定位，凭借标准化的特性具备广泛适用性，最适合集成到 RESTful API 的请求响应流程、微服务间的跨服务通信，
# 以及分布式系统中的数据传输场景，能适配多种复杂的架构需求。
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



async def async_main(mode):
    """异步主函数"""
    try:
        root_agent = create_agent(mode)
        # 创建会话服务
        session_service = InMemorySessionService()
        # 创建会话
        session = await session_service.create_session(
            user_id="user",
            state={},
            app_name="gaode_assistant"  # 添加必需的app_name参数
        )
        
        # 创建运行器
        runner = Runner(
            app_name="gaode_assistant",
            agent=root_agent,
            session_service=session_service,
            artifact_service=InMemoryArtifactService(),  # 可选
        )
        
        # 用户查询
        user_query = "帮我规划从北京到上海的路线，并查询上海的天气情况"
        
        print(f"\n用户查询: {user_query}\n")
        
        # 运行代理
        events = runner.run_async(
            user_id="user",
            session_id=session.id,
            run_config=sse_config,
            new_message=types.Content(role='user', parts=[types.Part(text=user_query)]),
        )
        
        # 处理事件
        final_response = None
        try:
            async for event in events:
                if event.is_final_response():
                    final_response = event.content.parts[0].text
                    break
        finally:
            # 显式关闭异步生成器以确保清理代码（如OpenTelemetry上下文的分离）能够正确执行。
            # 这有助于防止 'ValueError: ... was created in a different Context' 错误。
            await events.aclose()
        
        # 打印结果
        print("\n=== 回复 ===")
        print(final_response)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

def main():
    """主函数"""
    import argparse
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="高德地图助手")
    parser.add_argument("--connection", choices=["stdio", "sse", "streamable_http"], default="streamable_http", 
                       help="连接方式 (默认: stdio)")
    args = parser.parse_args()
    mode = args.connection
    # 运行异步主函数
    asyncio.run(async_main(mode))

if __name__ == "__main__":
    main()
