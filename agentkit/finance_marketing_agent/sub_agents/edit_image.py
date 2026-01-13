import logging
from veadk import Agent
from veadk.tools.builtin_tools.image_generate import image_generate
from prompts import GENERATE_IMAGE_AGENT_PROMPT

# 设置日志
logger = logging.getLogger(__name__)

edit_image_agent = Agent(
    name="edit_image_agent",
    description="消费金融营销图片生成专家，负责根据底图和设计要求生成高质量的营销素材",
    instruction=GENERATE_IMAGE_AGENT_PROMPT,
    tools=[image_generate],
    version="1.0.0",
)

logger.info("图片生成智能体初始化成功")
