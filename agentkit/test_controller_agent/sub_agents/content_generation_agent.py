from veadk import Agent

# 导入提示词
from ..prompts import CONTENT_GENERATION_AGENT_PROMPT

# 内容生成子智能体，负责根据用户需求生成各种类型的内容
content_generation_agent = Agent(
    name="content_generation_agent",
    description="内容生成智能体，负责根据用户需求生成各种类型的内容",
    instruction=CONTENT_GENERATION_AGENT_PROMPT,
    tools=[],
    version="1.0.0",
)
