from veadk import Agent, Runner
from veadk.memory.short_term_memory import ShortTermMemory

app_name = "veadk_playground_app"
user_id = "veadk_playground_user"
session_id = "veadk_playground_session"

short_term_memory = ShortTermMemory()

# sub agents
python_coding_agent = Agent(
    name="python_coder",
    description="擅长使用 Python 编程语言来解决问题。",
    instruction="""使用 Python 语言来解决问题。
    注意，你生成的代码第一行需要有注释，标明作者是`python-coder`。""",
)

java_coding_agent = Agent(
    name="java_coder",
    description="擅长使用 Java 编程语言来解决问题。",
    instruction="""使用 Java 语言来解决问题。
    注意，你生成的代码第一行需要有注释，标明作者是`java-coder`。""",
)

# root agent
coding_agent = Agent(
    name="coding_agent",
    description="可以调用适合的智能体来解决用户问题。",
    instruction="调用适合的智能体来解决用户问题。",
    sub_agents=[python_coding_agent, java_coding_agent],
)

runner = Runner(
    agent=coding_agent,
    short_term_memory=short_term_memory,
    app_name=app_name,
    user_id=user_id,
)

async def main():
    response = await runner.run(
        messages="使用 Python 帮我写一段快速排序的代码。", session_id=session_id
    )
    print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
