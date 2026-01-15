import logging
from veadk import Agent
from prompts import IMG_KB_QUERY_REWRITING_AGENT_PROMPT

# 设置日志
logger = logging.getLogger(__name__)

kb_query_rewriting_agent = Agent(
    name="kb_query_rewriting_agent",
    description="营销素材查询改写智能体",
    instruction=IMG_KB_QUERY_REWRITING_AGENT_PROMPT,
    version="1.0.0",
)

logger.info("预处理智能体初始化成功")
