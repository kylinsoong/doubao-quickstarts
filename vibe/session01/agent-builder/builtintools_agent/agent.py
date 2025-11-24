import asyncio

from veadk import Runner
from veadk.agent_builder import AgentBuilder

agent_builder = AgentBuilder()

agent = agent_builder.build(path="builtintools_agent/agent.yaml")

root_agent = agent

# runner = Runner(agent)# runner = Runner(agent)
# response = asyncio.run(runner.run("北京天气"))

# print(response)
# response = asyncio.run(runner.run("北京天气"))

# print(response)
