import logging
from veadk import Agent
from custom_tools import knowledge_service_search
from prompts import PROMOTIONAL_SEARCH_KB_AGENT_PROMPT

# 设置日志
logger = logging.getLogger(__name__)

promotional_search_kb_agent = Agent(
    name="promotional_search_kb_agent",
    description="搜索知识库，返回相关营销图片或视频链接",
    instruction=PROMOTIONAL_SEARCH_KB_AGENT_PROMPT,
    tools=[knowledge_service_search],
    version="1.0.0",
)

logger.info("知识库搜索智能体初始化成功")



