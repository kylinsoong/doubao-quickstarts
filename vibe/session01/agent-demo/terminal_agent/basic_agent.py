from veadk import Agent, Runner
from veadk.memory.short_term_memory import ShortTermMemory
from veadk.tools.demo_tools import get_city_weather

app_name = "veadk_playground_app"
user_id = "veadk_playground_user"
session_id = "veadk_playground_session"

# Define the DatetimeAgent
WeatherAgent = Agent(
    name="WeatherAgent",
    description="An agent that can report the weather of a city.",
    instruction="You are a helpful assistant that provides a city's weather.",
    tools=[get_city_weather],
)

short_term_memory = (
    ShortTermMemory()
)  # Short-term memory represents the conversation history within a single user session

runner = Runner(
    agent=WeatherAgent,
    short_term_memory=short_term_memory,
    app_name=app_name,
    user_id=user_id,
)


# Use the `run` method in the runner to call the Agent
async def main():
    response = await runner.run(
        messages="你好，请问北京的天气如何？", session_id=session_id
    )
    print(response)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
