import logging
from veadk import Agent
from custom_tools import knowledge_service_add_file
from prompts import SAVE_FILE_TO_KB_AGENT_PROMPT

# 设置日志
logger = logging.getLogger(__name__)

save_file_to_kb_agent = Agent(
    name="save_file_to_kb_agent",
    description="知识库文件保存专家，负责使用knowledge_service_add_file工具将图片或视频保存到知识库",
    instruction=SAVE_FILE_TO_KB_AGENT_PROMPT,
    tools=[knowledge_service_add_file],
    version="1.0.0",
)

logger.info("知识库文件保存智能体初始化成功")
