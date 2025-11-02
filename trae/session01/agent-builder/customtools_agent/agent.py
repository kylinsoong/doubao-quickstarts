import asyncio

from veadk import Runner
from veadk.agent_builder import AgentBuilder

agent_builder = AgentBuilder()

agent = agent_builder.build(path="customtools_agent/agent.yaml")

root_agent = agent

# runner = Runner(agent)
# response = asyncio.run(runner.run("roll a die and check prime numbers"))

# print(response)
