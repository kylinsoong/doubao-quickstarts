import logging
import re
from copy import deepcopy
from typing import Any, Dict, Optional

from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from google.genai.types import Content, Part

logger = logging.getLogger(__name__)


def after_tool_callback(
    tool: BaseTool,
    args: Dict[str, Any],
    tool_context: ToolContext,
    tool_response: Dict,
    **kwargs,
) -> Optional[Dict]:
    logger.info("after_tool_callback invoked for tool: %s, tool_response: %s", tool.__class__.__name__, tool_response)
    return None
