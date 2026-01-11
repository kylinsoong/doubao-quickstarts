from agentkit.apps import AgentkitAgentServerApp
from veadk import Agent, Runner
from veadk.memory.short_term_memory import ShortTermMemory
#from custom_tools import knowledge_service_search
from .custom_tools import knowledge_service_search

app_name = "veadk_playground_app_short_term_local"
user_id = "veadk_playground_user_short_term_local"
session_id = "veadk_playground_session_short_term_local"



root_agent = Agent(
    name="all_in_one_agent",
    description="all in one agent",
    instruction="""你是一个工具调用助手，严格按照插件返回的结构话内容回复，不做任何编辑""",
    tools=[knowledge_service_search],
)

short_term_memory = ShortTermMemory(backend="local")

runner = Runner(
    agent=root_agent,
    short_term_memory=short_term_memory,
    app_name=app_name,
    user_id=user_id,
)


async def main():
    response1 = await runner.run(messages="我叫VeADK", session_id=session_id)
    print(f"response of round 1: {response1}")

    response2 = await runner.run(messages="你还记得我叫什么吗？", session_id=session_id)
    print(f"response of round 2: {response2}")


# using veadk web for debugging
# root_agent = agent

agent_server_app = AgentkitAgentServerApp(
    agent=root_agent,
    short_term_memory=short_term_memory,
)

if __name__ == "__main__":
    agent_server_app.run(host="0.0.0.0", port=8000)
