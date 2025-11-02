from veadk import Agent, Runner
from veadk.memory.short_term_memory import ShortTermMemory
from veadk.tools.builtin_tools.web_search import web_search

app_name = "veadk_playground_app"
user_id = "veadk_playground_user"
session_id = "veadk_playground_session"

agent = Agent(
    name="SearchAgent",
    description="An agent that can search the web.",
    instruction="You are a helpful assistant that can search the web.",
    tools=[web_search]
)
short_term_memory = ShortTermMemory()

runner = Runner(
    agent=agent, short_term_memory=short_term_memory, app_name=app_name, user_id=user_id
)

async def main():
    response = await runner.run(
        messages="帮我搜索一下今天top3的新闻", session_id=session_id
    )
    print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
