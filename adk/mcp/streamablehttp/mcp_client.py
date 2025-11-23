from veadk import Agent, Runner
from veadk.memory.short_term_memory import ShortTermMemory
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset

app_name = "veadk_playground_app"
user_id = "veadk_playground_user"
session_id = "veadk_playground_session"

agent = Agent(
    name="WeatherAgent",
    description="An agent that can report the weather of a city.",
    instruction="You are a helpful assistant that provides a city's weather.",
    tools=[MCPToolset(
        connection_params=StreamableHTTPServerParams(
            url='http://localhost:9000/mcp',
        ),
    )],
)

short_term_memory = ShortTermMemory()

runner = Runner(
    agent=agent,
    short_term_memory=short_term_memory,
    app_name=app_name,
    user_id=user_id,
)

async def main():
    response = await runner.run(
        messages="你好，请问北京的天气如何？", session_id=session_id
    )
    print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
