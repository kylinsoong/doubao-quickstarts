from veadk import Agent
from veadk.tools.builtin_tools.image_generate import image_generate
from prompts import GENERATE_IMAGE_AGENT_PROMPT

generate_image_agent = Agent(
    name="generate_image_agent",
    description="generate image agent",
    instruction=GENERATE_IMAGE_AGENT_PROMPT,
    tools=[image_generate],
)
