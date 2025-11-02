import asyncio

from veadk.agent_builder import AgentBuilder

agent_builder = AgentBuilder()

agent = agent_builder.build(path="basic_agent/agent.yaml")

root_agent = agent

# runner = Runner(agent)
# response = asyncio.run(runner.run("你好"))

# print(response)
