import logging
from typing import Optional

from google.adk.agents.callback_context import CallbackContext
from google.genai import types
from google.genai.types import Content

logger = logging.getLogger(__name__)


def after_model_callback(
    callback_context: CallbackContext, llm_response: Content, **kwargs
) -> Optional[types.Content]:
    logger.info("after_model_callback invoked，llm_response: %s", llm_response)
    return None
