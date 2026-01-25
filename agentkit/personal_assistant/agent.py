import asyncio
import os

from veadk import Agent, Runner 
from veadk.knowledgebase import KnowledgeBase  
from veadk.memory import LongTermMemory, ShortTermMemory  
from veadk.tools.builtin_tools.run_code import run_code  
from veadk.tools.builtin_tools.mcp_router import mcp_router  
from google.adk.agents.callback_context import CallbackContext 
from dotenv import load_dotenv

load_dotenv()

memory_name = os.getenv("DATABASE_VIKINGMEM_COLLECTION")
if not memory_name:
    raise ValueError("DATABASE_VIKINGMEM_COLLECTION environment variable is not set")

# 使用viking作为长期记忆存储，可按需切换 mem0
long_term_memory = LongTermMemory(backend="viking", index=memory_name)

# 使用本地内存作为短期记忆，如需持久化backend可配置为mysql，需提前在火山创建数据库
short_term_memory = ShortTermMemory(backend="local")

knowledge_name = os.getenv("DATABASE_VIKING_COLLECTION")
if not knowledge_name:
    raise ValueError("DATABASE_VIKING_COLLECTION environment variable is not set")

# 使用viking作为知识库存储
knowledgebase = KnowledgeBase(backend="viking", index=knowledge_name)

# 定义异步回调函数，用于在代理执行完成后获取当前会话并将其添加到长期记忆存储中
async def after_agent_execution(callback_context: CallbackContext):
    session = callback_context._invocation_context.session
    await long_term_memory.add_session_to_memory(session)

# 定义个人助手Agent
personal_assistant = Agent(
    name="personal_assistant",
    description="一个智能个人助手，可以帮助用户管理日常事务和提供信息。",
    instruction="""
你是一个友好的智能个人助手，请用简洁明了的语言回答用户的问题。
如果用户询问与知识库相关的信息，请使用知识库检索。
如果用户提到个人偏好或重要信息，请将其存储到长期记忆中。
如果需要执行代码生成任务，请使用代码沙箱工具。
如果需要执行其他任务，请选取合适的MCP工具。
""",
    short_term_memory=short_term_memory,
    long_term_memory=long_term_memory, 
    knowledgebase=knowledgebase,
    tools=[run_code, mcp_router],
    after_agent_callback=after_agent_execution,
)

# 使用veadk web进行调试
root_agent = personal_assistant

async def main():
    """运行个人助手的主函数"""
    print("欢迎使用智能个人助手！")
    print("输入 'exit' 或 'quit' 退出程序。")
    print("=" * 50)
    
    # 创建智能体运行器
    runner = Runner(
        agent=personal_assistant,
        app_name="personal_assistant_demo",
        user_id="demo_user",
        short_term_memory=short_term_memory
    )

    while True:
        user_input = input("请输入您的问题: ")
        
        if user_input.lower() in ["exit", "quit", "退出"]:
            print("再见！")
            break
        
        try:
            # 运行agent并获取响应
            response = await runner.run(messages=user_input)
            print(f"助手: {response}")
        except Exception as e:
            print(f"发生错误: {e}")
        
        print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())