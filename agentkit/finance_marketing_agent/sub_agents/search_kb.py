import logging
from veadk import Agent
from custom_tools import knowledge_service_search
from prompts import SEARCH_KB_AGENT_PROMPT

# 设置日志
logger = logging.getLogger(__name__)

search_kb_agent = Agent(
    name="search_kb_agent",
    description="知识服务搜索专家，负责使用knowledge_service_search工具查询知识库并返回相关图片链接",
    instruction=SEARCH_KB_AGENT_PROMPT,
    tools=[knowledge_service_search],
    version="1.0.0",
)

logger.info("知识库搜索智能体初始化成功")



