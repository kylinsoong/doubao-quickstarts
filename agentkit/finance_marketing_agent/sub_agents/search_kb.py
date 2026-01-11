from veadk import Agent
from custom_tools import knowledge_service_search
from prompts import SEARCH_KB_AGENT_PROMPT

search_kb_agent =  Agent(
    name="search_kb_agent",
    description="search kb agent",
    instruction=SEARCH_KB_AGENT_PROMPT,
    tools=[knowledge_service_search],
)



