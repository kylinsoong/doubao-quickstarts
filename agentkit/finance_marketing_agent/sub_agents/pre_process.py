import logging
from veadk import Agent
from prompts import PRE_PROCESS_AGENT_PROMPT

# 设置日志
logger = logging.getLogger(__name__)

pre_process_agent = Agent(
    name="pre_process_agent",
    description="消费金融营销需求分析师，负责从用户问题中提取查询知识库的关键词和生成营销素材的具体要求",
    instruction=PRE_PROCESS_AGENT_PROMPT,
    version="1.0.0",
)

logger.info("预处理智能体初始化成功")
