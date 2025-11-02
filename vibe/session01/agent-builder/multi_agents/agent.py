import asyncio

from veadk import Runner
from veadk.agent_builder import AgentBuilder

agent_builder = AgentBuilder()

agent = agent_builder.build(path="multi_agents/agent.yaml")

root_agent = agent

# runner = Runner(agent)
# response = asyncio.run(runner.run("北京穿衣建议"))

# print(response)
