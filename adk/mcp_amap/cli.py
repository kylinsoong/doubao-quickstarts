from veadk import Runner
from veadk.memory.short_term_memory import ShortTermMemory
from agent import root_agent

app_name = "mcp_gaode_cli_app"
user_id = "mcp_gaode_cli_user"
session_id = "mcp_gaode_cli_session"

short_term_memory = (
    ShortTermMemory()
)

runner = Runner(
    agent=root_agent,
    short_term_memory=short_term_memory,
    app_name=app_name,
    user_id=user_id,
)


async def main():
    response = await runner.run(
        messages="帮我规划从北京到上海的路线", session_id=session_id
    )
    print(response)



if __name__ == "__main__":
    import asyncio

    asyncio.run(main())


