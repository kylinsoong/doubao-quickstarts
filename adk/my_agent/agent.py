from veadk import Agent
from veadk.memory.short_term_memory import ShortTermMemory
from veadk.tools.demo_tools import get_city_weather

app_name = "my_agent_app"
user_id = "my_agent_user"
session_id = "my_agent_session"

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

root_agent = WeatherAgent



