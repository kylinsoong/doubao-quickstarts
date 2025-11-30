import asyncio
import json
import os
import logging

from mcp import types as mcp_types  
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions

import mcp.server.stdio

from google.adk.tools.function_tool import FunctionTool
from veadk.tools.demo_tools import get_city_weather

from google.adk.tools.mcp_tool.conversion_utils import adk_to_mcp_tool_type

# 获取脚本所在的目录
log_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(log_dir, "output.log")

# 配置日志记录器
log_formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

# 文件处理器 - DEBUG
file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(log_formatter)
root_logger.addHandler(file_handler)

# 控制台处理器 - INFO
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(log_formatter)
root_logger.addHandler(console_handler)

# --- 步骤1: 准备要通过MCP暴露的ADK工具 ---
logging.info("正在初始化ADK工具: get_city_weather...")
adk_tool_to_expose = FunctionTool(get_city_weather)
logging.info(f"ADK工具 '{adk_tool_to_expose.name}' 初始化完成，准备通过 MCP 暴露。")


# --- 步骤2: 设置MCP服务器 ---
# 
logging.info("正在创建MCP服务器实例...")
app = Server("adk-tool-exposing-mcp-server")


# 实现MCP服务器的 `list_tools` 方法，用于向客户端宣告本服务器提供了哪些工具。
@app.list_tools()
async def list_mcp_tools() -> list[mcp_types.Tool]:
    """此函数作为MCP的处理器，用于列出本服务器暴露的所有工具。"""
    logging.info("MCP服务器: 收到 `list_tools` 请求。")

    # 使用 `adk_to_mcp_tool_type` 工具函数将ADK工具的定义转换为MCP的工具模式。
    mcp_tool_schema = adk_to_mcp_tool_type(adk_tool_to_expose)
    logging.info(f"MCP服务器: 宣告工具: {mcp_tool_schema.name}")
    return [mcp_tool_schema]


# 实现MCP服务器的 `call_tool` 方法，用于执行客户端请求的工具调用。
@app.call_tool()
async def call_mcp_tool(name: str, arguments: dict) -> list[mcp_types.Content]:
    """此函数作为MCP的处理器，用于执行客户端请求的工具调用。"""
    logging.info(f"MCP服务器: 收到对工具 '{name}' 的调用请求，参数为: {arguments}")

    # 检查请求的工具名是否与我们暴露的ADK工具匹配。
    if name == adk_tool_to_expose.name:
        try:
            # 异步执行ADK工具的 `run_async` 方法。
            # 注意：这里的 `tool_context` 为 `None`，因为此MCP服务器是在一个完整的ADK Runner之外独立运行ADK工具的。
            # 如果ADK工具的运行依赖于 `ToolContext` 提供的特性（如状态管理或认证），
            # 这种直接调用可能需要更复杂的处理逻辑。
            adk_tool_response = await adk_tool_to_expose.run_async(
                args=arguments,
                tool_context=None,
            )
            logging.info(f"MCP服务器: ADK工具 '{name}' 执行完毕。响应: {adk_tool_response}")

            # 将ADK工具的响应（通常是一个字典）格式化为MCP兼容的格式。
            # 在这里，我们将响应字典序列化为JSON字符串，并封装在 `TextContent` 中。
            # 具体的格式化方式应根据ADK工具的输出和客户端的需求进行调整。
            response_text = json.dumps(adk_tool_response, indent=2)

            # MCP期望返回一个 `mcp_types.Content` 的列表。
            return [mcp_types.TextContent(type="text", text=response_text)]

        except Exception as e:
            logging.error(f"MCP服务器: 执行ADK工具 '{name}' 时出错: {e}")
            # 以MCP格式返回错误信息。
            error_text = json.dumps({
                "error": f"执行工具 '{name}' 失败: {str(e)}"
            })
            return [mcp_types.TextContent(type="text", text=error_text)]
    else:
        # 处理调用未知工具的情况。
        logging.error(f"MCP服务器: 此服务器未找到或未暴露工具 '{name}'。")
        error_text = json.dumps({
            "error": f"此服务器未实现工具 '{name}'。"
        })
        return [mcp_types.TextContent(type="text", text=error_text)]


# --- 步骤3: 运行MCP服务器 ---
async def run_mcp_stdio_server():
    """运行MCP服务器，通过标准输入/输出（stdio）监听连接。"""
    # 使用 `mcp.server.stdio` 库提供的 `stdio_server` 上下文管理器。
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logging.info("MCP Stdio服务器: 正在与客户端进行握手...")
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=app.name,  # 使用上面定义的服务名
                server_version="0.1.0",
                capabilities=app.get_capabilities(
                    # 定义服务器的能力，具体选项请参考MCP文档。
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
        logging.info("MCP Stdio服务器: 运行循环结束或客户端已断开连接。")


if __name__ == "__main__":
    logging.info("正在通过stdio启动MCP服务器以暴露ADK工具...")
    try:
        asyncio.run(run_mcp_stdio_server())
    except KeyboardInterrupt:
        logging.info("\nMCP服务器 (stdio) 已被用户停止。")
    except Exception as e:
        logging.info(f"MCP服务器 (stdio) 遇到错误: {e}")
    finally:
        logging.info("MCP服务器 (stdio) 进程退出。")
