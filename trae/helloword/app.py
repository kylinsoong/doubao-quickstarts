from test_agent.agent import root_agent
from veadk import Runner

app_name = "veadk_playground_app"
user_id = "veadk_playground_user"
session_id = "veadk_playground_session"

runner = Runner(
    agent=root_agent, app_name=app_name, user_id=user_id
)

async def main():
    response = await runner.run(
        messages="你好，请问你可以做什么？", session_id=session_id
    )
    print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
