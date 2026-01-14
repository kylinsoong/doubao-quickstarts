from veadk import Agent
from veadk.tools.builtin_tools.image_generate import image_generate
from prompts import IMAGEOTIONAL_IMAGE_GENERATE_AGENT_PROMPT

promotional_image_generate_agent = Agent(
    name="promotional_image_generate_agent",
    description="图片生成专家，负责根据用户需求生成图片",
    instruction=IMAGEOTIONAL_IMAGE_GENERATE_AGENT_PROMPT,
    tools=[image_generate],
    version="1.0.0",
)