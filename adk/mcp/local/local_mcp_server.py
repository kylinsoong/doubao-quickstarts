# local_mcp_server.py
# 这是一个MCP（Machine-to-Machine Communication Protocol）服务器的示例，
# 它将一个ADK（Agent Development Kit）工具（`load_web_page`）封装并通过MCP协议暴露出去，
# 允许其他兼容MCP的客户端（如另一个Agent）远程调用这个工具。

import asyncio
import json
import sys

# 导入MCP服务器相关库
from mcp import types as mcp_types  # 使用别名以避免与ADK的类型冲突
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions

# 导入MCP的stdio服务器，用于通过标准输入/输出运行服务器
import mcp.server.stdio

# 导入ADK工具相关库
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.load_web_page import load_web_page  # 这是一个ADK提供的示例工具

# 导入ADK与MCP之间的转换工具
from google.adk.tools.mcp_tool.conversion_utils import adk_to_mcp_tool_type

# --- 步骤1: 准备要通过MCP暴露的ADK工具 ---
# 实例化你想要暴露的ADK工具。这个工具将被MCP服务器封装，并响应来自客户端的调用。
print("正在初始化ADK工具: load_web_page...", file=sys.stderr)
adk_tool_to_expose = FunctionTool(load_web_page)
print(f"ADK工具 '{adk_tool_to_expose.name}' 初始化完成，准备通过MCP暴露。", file=sys.stderr)


# --- 步骤2: 设置MCP服务器 ---
# 创建一个MCP服务器实例，并为其命名。
print("正在创建MCP服务器实例...", file=sys.stderr)
app = Server("adk-tool-exposing-mcp-server")


# 实现MCP服务器的 `list_tools` 方法，用于向客户端宣告本服务器提供了哪些工具。
@app.list_tools()
async def list_mcp_tools() -> list[mcp_types.Tool]:
    """此函数作为MCP的处理器，用于列出本服务器暴露的所有工具。"""
    print("MCP服务器: 收到 `list_tools` 请求。", file=sys.stderr)

    # 使用 `adk_to_mcp_tool_type` 工具函数将ADK工具的定义转换为MCP的工具模式。
    mcp_tool_schema = adk_to_mcp_tool_type(adk_tool_to_expose)
    print(f"MCP服务器: 宣告工具: {mcp_tool_schema.name}", file=sys.stderr)
    return [mcp_tool_schema]


# 实现MCP服务器的 `call_tool` 方法，用于执行客户端请求的工具调用。
@app.call_tool()
async def call_mcp_tool(name: str, arguments: dict) -> list[mcp_types.Content]:
    """此函数作为MCP的处理器，用于执行客户端请求的工具调用。"""
    print(f"MCP服务器: 收到对工具 '{name}' 的调用请求，参数为: {arguments}", file=sys.stderr)

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
            print(f"MCP服务器: ADK工具 '{name}' 执行完毕。响应: {adk_tool_response}", file=sys.stderr)

            # 将ADK工具的响应（通常是一个字典）格式化为MCP兼容的格式。
            # 在这里，我们将响应字典序列化为JSON字符串，并封装在 `TextContent` 中。
            # 具体的格式化方式应根据ADK工具的输出和客户端的需求进行调整。
            response_text = json.dumps(adk_tool_response, indent=2)

            # MCP期望返回一个 `mcp_types.Content` 的列表。
            return [mcp_types.TextContent(type="text", text=response_text)]

        except Exception as e:
            print(f"MCP服务器: 执行ADK工具 '{name}' 时出错: {e}", file=sys.stderr)
            # 以MCP格式返回错误信息。
            error_text = json.dumps({
                "error": f"执行工具 '{name}' 失败: {str(e)}"
            })
            return [mcp_types.TextContent(type="text", text=error_text)]
    else:
        # 处理调用未知工具的情况。
        print(f"MCP服务器: 此服务器未找到或未暴露工具 '{name}'。", file=sys.stderr)
        error_text = json.dumps({
            "error": f"此服务器未实现工具 '{name}'。"
        })
        return [mcp_types.TextContent(type="text", text=error_text)]


# --- 步骤3: 运行MCP服务器 ---
async def run_mcp_stdio_server():
    """运行MCP服务器，通过标准输入/输出（stdio）监听连接。"""
    # 使用 `mcp.server.stdio` 库提供的 `stdio_server` 上下文管理器。
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        print("MCP Stdio服务器: 正在与客户端进行握手...", file=sys.stderr)
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
        print("MCP Stdio服务器: 运行循环结束或客户端已断开连接。", file=sys.stderr)


if __name__ == "__main__":
    print("正在通过stdio启动MCP服务器以暴露ADK工具...", file=sys.stderr)
    try:
        asyncio.run(run_mcp_stdio_server())
    except KeyboardInterrupt:
        print("\nMCP服务器 (stdio) 已被用户停止。", file=sys.stderr)
    except Exception as e:
        print(f"MCP服务器 (stdio) 遇到错误: {e}", file=sys.stderr)
    finally:
        print("MCP服务器 (stdio) 进程退出。", file=sys.stderr)
