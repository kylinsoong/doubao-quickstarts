import logging
from veadk import Agent
from veadk.tools.builtin_tools.image_generate import image_generate
from prompts import PROMOTIONAL_EDIT_IMAGE_AGENT_PROMPT

# 设置日志
logger = logging.getLogger(__name__)

promotional_image_modify_agent = Agent(
    name="promotional_image_modify_agent",
    description="消费金融营销图片修改专家，负责修改已有的营销图片",
    instruction=PROMOTIONAL_EDIT_IMAGE_AGENT_PROMPT,
    tools=[image_generate],
    version="1.0.0",
)

logger.info("图片生成智能体初始化成功")
