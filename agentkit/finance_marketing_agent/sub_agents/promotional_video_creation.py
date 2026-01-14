from veadk import Agent
from veadk.tools.builtin_tools.video_generate import video_generate

from prompts import PROMOTIONAL_VEDIO_GENERATION_AGENT_PROMPT

promotional_video_creation_agent = Agent(
    name="promotional_video_creation_agent",
    description="营销视频创作智能体，负责根据用户需求创作营销视频",
    instruction=PROMOTIONAL_VEDIO_GENERATION_AGENT_PROMPT,
    tools=[video_generate],
    version="1.0.0",
)
