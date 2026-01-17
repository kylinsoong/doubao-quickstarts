from veadk import Agent

# 导入提示词
from ..prompts import INFO_RETRIEVAL_AGENT_PROMPT

# 信息检索子智能体，负责从各种来源检索相关信息
info_retrieval_agent = Agent(
    name="info_retrieval_agent",
    description="信息检索智能体，负责从各种来源检索相关信息",
    instruction=INFO_RETRIEVAL_AGENT_PROMPT,
    tools=[],
    version="1.0.0",
)
