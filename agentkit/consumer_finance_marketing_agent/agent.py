import os
import sys

from agentkit.apps import AgentkitAgentServerApp
from veadk import Agent, Runner
from veadk.memory.short_term_memory import ShortTermMemory


# Add current directory to Python path to support sub_agents imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from prompts import CUONSUMER_FINANCE_MARKETING_AGENT_PROMPT, PRE_PROCESS_AGENT_PROMPT
#from sub_agents.sequential_agent import sequential_service_agent

short_term_memory = ShortTermMemory(
    backend="local"
)

pre_process_agent = Agent(
    name="pre_process_agent",
    description="消费金融营销助手，负责从用户问题中提取插叙知识库的Query信息，以及获取生成营销素材的相关的要求",
    instruction=PRE_PROCESS_AGENT_PROMPT,
)

consumer_finance_marketing_agent = Agent(
    name="consumer_finance_marketing_agent",
    description="消费金融营销助手，根据用户问题，生成相应的营销素材",
    instruction= CUONSUMER_FINANCE_MARKETING_AGENT_PROMPT,
    sub_agents=[pre_process_agent],
)

root_agent = consumer_finance_marketing_agent

runner = Runner(agent=root_agent)

agent_server_app = AgentkitAgentServerApp(
    agent=root_agent,
    short_term_memory=short_term_memory,
)

if __name__ == "__main__":
    agent_server_app.run(host="0.0.0.0", port=8000)