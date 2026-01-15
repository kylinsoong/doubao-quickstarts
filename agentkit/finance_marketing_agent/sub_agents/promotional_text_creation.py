from veadk import Agent

# 导入提示词
from prompts import PROMOTIONAL_TEXT_GENERATION_AGENT_PROMPT

# 内容生成子智能体，负责根据用户需求生成各种类型的内容
promotional_text_creation_agent = Agent(
    name="promotional_text_creation_agent",
    description="营销文案创作智能体，负责根据用户需求创作营销文案",
    instruction=PROMOTIONAL_TEXT_GENERATION_AGENT_PROMPT,
    tools=[],
    version="1.0.0",
)
