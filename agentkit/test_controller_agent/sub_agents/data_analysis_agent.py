from veadk import Agent

# 导入提示词
from ..prompts import DATA_ANALYSIS_AGENT_PROMPT

# 数据分析子智能体，负责处理和分析各种数据
data_analysis_agent = Agent(
    name="data_analysis_agent",
    description="数据分析智能体，负责处理和分析各种数据",
    instruction=DATA_ANALYSIS_AGENT_PROMPT,
    tools=[],
    version="1.0.0",
)
