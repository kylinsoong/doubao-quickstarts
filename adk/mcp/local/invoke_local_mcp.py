# ./adk_agent_samples/mcp_client_agent/agent.py
import os
import builtins
from veadk.agent import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

# IMPORTANT: Replace this with the ABSOLUTE path to your local_mcp_server.py script
PATH_TO_YOUR_MCP_SERVER_SCRIPT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "local_mcp_server.py",
    )
)

root_agent = Agent(
    name='web_reader_mcp_client_agent',
    instruction="Use the 'load_web_page' tool to fetch content from a URL provided by the user.",
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params = StdioServerParameters(
                    command='python3', # Command to run your MCP server script
                    args=[PATH_TO_YOUR_MCP_SERVER_SCRIPT], # Argument is the path to the script
                )
            )
            # tool_filter=['load_web_page'] # Optional: ensure only specific tools are loaded
        )
    ],
)

async def test_agent_calls():
    response = await root_agent.run("你能做什么？")
    print(f"Agent响应: {response}\n")
    response = await root_agent.run("总结下 https://www.volcengine.com/ 最近有什么关键的重大更新，总结出来5项最关键的。")
    print(f"Agent响应: {response}\n")
    
    
import unittest
import asyncio

# An integration test to ensure the agent can communicate with the MCP server
class TestAgentMCPIntegration(unittest.TestCase):
    def test_agent_can_load_volcengine(self):
        async def run_test():
            response = await root_agent.run("总结下 https://www.volcengine.com/ 最近有什么关键的重大更新，总结出来5项最关键的。")
            self.assertIn("豆包", response)

        asyncio.run(run_test())

    def test_assert_supported_tools(self):
        async def run_test():
            # The MCPToolset is the first tool in our agent's tool list
            mcp_toolset = root_agent.tools[0]
            
            # Get the list of tools from the MCP server
            supported_tools = await mcp_toolset.get_tools()
            
            # Assert that there is one tool supported
            self.assertEqual(len(supported_tools), 1)
            
            # Get the tool
            the_tool = supported_tools[0]
            
            # Assert the tool's name
            self.assertEqual(the_tool.name, "load_web_page")
            
            # Assert the tool's description (or part of it)
            self.assertIn("Fetches the content in the url", the_tool.description)

            # Assert the tool's parameters
            self.assertIn("url", the_tool.raw_mcp_tool.inputSchema["properties"])
            url_param = the_tool.raw_mcp_tool.inputSchema["properties"]["url"]
            self.assertEqual(url_param["type"], "string")
            self.assertIn("url", the_tool.raw_mcp_tool.inputSchema["required"])

        asyncio.run(run_test())

def run_tests():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestAgentMCPIntegration))
    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == "__main__":
    run_tests()
