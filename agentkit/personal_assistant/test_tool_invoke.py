from veadk import Agent, Runner
import asyncio
from veadk.tools.builtin_tools.run_code import run_code

agent: Agent = Agent(
    tools=[run_code],
)

runner = Runner(agent=agent)
built_in_tools_session = "built_in_tools_session"
user_prompt = "给我一个 50 和 100 之间的随机质数"
response = asyncio.run(
    runner.run(messages=user_prompt, session_id=built_in_tools_session)
)
print(response)
