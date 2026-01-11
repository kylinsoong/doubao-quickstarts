import asyncio

from prompts import SEQUENTIAL_SERVICE_AGENT_PROMPT
from sub_agents.search_kb import search_kb_agent
from sub_agents.generate_image import generate_image_agent
from sub_agents.pre_process import pre_process_agent
from veadk import Runner
from veadk.agents.sequential_agent import SequentialAgent


sequential_service_agent = SequentialAgent(
    name="sequential_service_agent",
    description="根据用户需求，逐步执行工作流，生成最佳回复结果",
    instruction=SEQUENTIAL_SERVICE_AGENT_PROMPT,
    sub_agents=[pre_process_agent,search_kb_agent, generate_image_agent],
)