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

app_name = "veadk_playground_app"
user_id = "veadk_playground_user"
session_id = "veadk_playground_session"
short_term_memory = ShortTermMemory()

runner = Runner(
    agent=root_agent, short_term_memory=short_term_memory, app_name=app_name, user_id=user_id
)

async def main(messages: str):
    response = await runner.run(
        messages=messages, session_id=session_id
    )
    print(f"prompt: {messages}, response: {response}")

if __name__ == "__main__":
    import asyncio
    image_generate_prompt = "生成一只小狗图片，生成一个小狗飞上天抓金鱼的图片，最终合成一个480p的视频"
    prompt = image_generate_prompt
    asyncio.run(main(prompt))
