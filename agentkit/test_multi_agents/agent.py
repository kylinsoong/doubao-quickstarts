from veadk import Agent
from veadk.memory.short_term_memory import ShortTermMemory

# 导入子智能体（使用相对导入）
from .sub_agents.info_retrieval_agent import info_retrieval_agent
from .sub_agents.data_analysis_agent import data_analysis_agent
from .sub_agents.content_generation_agent import content_generation_agent

# 导入提示词（使用相对导入）
from .prompts import MAIN_AGENT_PROMPT

# 主智能体，负责根据用户意图选择合适的子智能体执行任务
tester_service_agent = Agent(
    name="tester_service_agent",
    description="测试服务主智能体，能够根据用户意图选择合适的子智能体执行任务",
    instruction=MAIN_AGENT_PROMPT,
    sub_agents=[info_retrieval_agent, data_analysis_agent, content_generation_agent],
    version="1.0.0",
)

root_agent = tester_service_agent
