from veadk import Runner
from veadk.memory.short_term_memory import ShortTermMemory
from agent import root_agent

app_name = "mcp_local_cli_app"
user_id = "mcp_local_cli_user"
session_id = "mcp_local_cli_session"

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
        messages="北京的天气怎么样", session_id=session_id
    )
    print(response)

    response = await runner.run(
        messages="上海的天气怎么样", session_id=session_id
    )
    print(response)



if __name__ == "__main__":
    import asyncio

    asyncio.run(main())


