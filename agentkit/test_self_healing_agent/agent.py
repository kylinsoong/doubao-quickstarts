
from veadk import Agent
from veadk.agents.loop_agent import LoopAgent
from veadk.utils.logger import get_logger
from google.adk.tools.tool_context import ToolContext


logger = get_logger(__name__)


from .prompts import WRITE_AGENT_PROMPT, EVALUATION_AGENT_PROMPT, LOOP_CONTROLLER_PROMPT


def exit_tool(tool_context: ToolContext) -> str:
    print(f"  [Tool Call] exit_loop triggered by {tool_context.agent_name}")
    tool_context.actions.end_of_agent = True
    return {}

write_agent = Agent(
    name="write_agent",
    description="负责撰写高质量的文档，结构完整、内容详实、表达流畅",
    instruction=WRITE_AGENT_PROMPT,
)
    
evaluation_agent = Agent(
    name="evaluation_agent",
    description="负责对撰写的文档进行全面的质量检查，确保文档符合所有标准",
    instruction=EVALUATION_AGENT_PROMPT,
)
    
loop_controller_agent = LoopAgent(
    name="loop_controller_agent",
    description="作为文案设计流程的统筹者，自动触发子Agent调用流程，直到文档质检合格",
    instruction=LOOP_CONTROLLER_PROMPT,
    sub_agents=[write_agent, evaluation_agent],
    tools=[exit_tool],
    max_iterations=1,  
)
    
root_agent = loop_controller_agent
