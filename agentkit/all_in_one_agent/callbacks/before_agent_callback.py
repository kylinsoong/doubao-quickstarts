import logging
from typing import Optional

from google.adk.agents.callback_context import CallbackContext
from google.genai import types

logger = logging.getLogger(__name__)


def before_agent_callback(
    agent, 
    messages, 
    session_id
) -> Optional[types.Content]:    
    logger.info(f"[before_agent_callback] Agent: {agent.name}, Messages: {messages}, Session ID: {session_id}")
    return None
