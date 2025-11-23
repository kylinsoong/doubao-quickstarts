from veadk import Agent, Runner
from veadk.memory.short_term_memory import ShortTermMemory
from veadk.tools.builtin_tools.image_generate import image_generate
from veadk.tools.builtin_tools.video_generate import video_generate


root_agent = Agent( 
    name="quick_video_create_agent",
    description=("You are an expert in creating images and video"),
    instruction="""You can create images and using the images to generate video. 
                """,
    tools=[image_generate, video_generate],
)

agent = root_agent
