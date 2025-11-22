"""
智能体回调函数模块
包含智能体生命周期各阶段的回调处理逻辑
"""
import logging
import re
from copy import deepcopy
from typing import Any, Dict, Optional

from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest, LlmResponse
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from google.genai.types import Content, Part

# 配置日志
logger = logging.getLogger(__name__)

# --- 敏感词黑名单 ---
BLOCKED_WORDS_CHINESE = [
    "zanghua",
    "minganci",
    "bukexiangdeshi",
]

# --- 个人信息(PII)过滤规则 ---
PII_PATTERNS_CHINESE = {
    '电话号码': r'1[3-9]\d{9}',
    '身份证号': r'\d{17}[\dXx]',  # 17位数字 + 1位数字或X
    '邮箱': r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}',
}


def filter_pii(text: str, patterns: Dict[str, str] = None, show_logs: bool = True) -> str:
    """
    过滤文本中的个人身份信息(PII)
    """
    if patterns is None:
        patterns = PII_PATTERNS_CHINESE
    
    filtered_text = text
    
    for pii_type, pattern_str in patterns.items():
        pattern = re.compile(pattern_str)
        
        def replace_and_log(match):
            found_pii = match.group(0)
            if show_logs:
                print(f"✓ 检测到 {pii_type}: {found_pii} → 已隐藏")
            return f"[{pii_type}已隐藏]"
        
        filtered_text = pattern.sub(replace_and_log, filtered_text)
    
    return filtered_text


def before_agent_callback(
    callback_context: CallbackContext,
) -> Optional[Content]:
    """在智能体开始处理用户请求前被调用"""
    user_input = ""
    if callback_context.user_content and callback_context.user_content.parts:
        last_message = callback_context.user_content.parts[-1]
        user_input = last_message.text if hasattr(last_message, "text") else ""

    logger.info(f"请求内容: {user_input[:50]}...          ")
    return None


def before_model_callback(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """在调用大语言模型（LLM）之前被调用"""
    logger.info("--- [模型调用前] 检查并修改输入内容 ---")
    agent_name = callback_context.agent_name
    logger.info(f"[Callback] Agent '{agent_name}' 正在准备调用模型。")

    # 提取最新的用户消息文本
    last_user_message = ""
    if llm_request.contents and llm_request.contents[-1].role == "user":
        if llm_request.contents[-1].parts:
            last_user_message = llm_request.contents[-1].parts[0].text or ""
    logger.info(f"[Callback] 检查用户最新消息: '{last_user_message}'")

    # 检查敏感词
    for word in BLOCKED_WORDS_CHINESE:
        if word.lower() in last_user_message.lower():
            logger.warning(f"检测到敏感词 '{word}'。已拦截该请求。")
            return LlmResponse(
                content=Content(
                    role="model",
                    parts=[
                        Part(text="很抱歉，您发送的内容包含不当言论，我无法处理。")
                    ],
                )
            )

    # 为系统指令添加前缀
    logger.info("内容安全，准备为系统指令添加前缀。")
    original_instruction = llm_request.config.system_instruction
    prefix = "[由回调函数修改] "

    original_text = ""
    if isinstance(original_instruction, Content) and original_instruction.parts:
        original_text = original_instruction.parts[0].text or ""
    elif isinstance(original_instruction, str):
        original_text = original_instruction

    modified_text = prefix + original_text
    llm_request.config.system_instruction = modified_text
    logger.info(f"[Callback] 已将系统指令修改为: '{modified_text}'")

    logger.info("[Callback] 继续执行模型调用。")
    return None


def after_model_callback(
    callback_context: CallbackContext, llm_response: Content, **kwargs
) -> Optional[Content]:
    """在从大语言模型（LLM）收到响应之后被调用"""
    logger.info("--- [模型调用后] ---")
    logger.debug(f"[Callback DEBUG] after_model_callback 接收到的 llm_response: {llm_response}")
    return None


def before_tool_callback(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, **kwargs
) -> Optional[Dict[str, Any]]:
    """在工具执行之前被调用"""
    tool_name = tool.name
    logger.info(f"--- [工具调用前] 校验 '{tool_name}' 工具的参数 ---")

    if tool_name == "write_article":
        word_count = args.get("word_count", 0)
        if not isinstance(word_count, int) or word_count <= 0:
            logger.warning(f"参数校验失败：word_count ({word_count}) 必须是正整数。")
            return {"result": "错误：文章字数必须为正整数。"}

    return None


def after_tool_callback(
    tool: "BaseTool",
    args: Dict[str, Any],
    tool_context: "ToolContext",
    tool_response: Dict,
    **kwargs,
) -> Optional[Dict]:
    """在工具调用之后被调用"""
    logger.info(f"  [工具结束] 工具 {tool.name} 已执行。")
    if tool.name == "write_article":
        response_text = deepcopy(tool_response)
    filtered_text = filter_pii(response_text)
    return Content(parts=[Part(text=filtered_text)])


def after_agent_callback(
    callback_context: CallbackContext
) -> Optional[Content]:
    """在智能体完成所有处理，即将结束会话时被调用"""
    logger.info("--- [智能体结束] ---")
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id

    print(f"\n[Callback] 智能体 '{agent_name}' (会话ID: {invocation_id}) 已结束。")
    return None
