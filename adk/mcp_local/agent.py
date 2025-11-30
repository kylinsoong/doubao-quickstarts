import os
from veadk.agent import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters, StdioConnectionParams

PATH_TO_YOUR_MCP_SERVER_SCRIPT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "local_mcp_server.py",
    )
)

root_agent = Agent(
    name='local_mcp_client_agent',
    instruction="Use the 'get_city_weather' tool to report the weather of a city.",
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params = StdioServerParameters(
                    command='python3', # Command to run your MCP server script
                    args=[PATH_TO_YOUR_MCP_SERVER_SCRIPT], # Argument is the path to the script
                )
            )
        )
    ],
)