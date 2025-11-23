# 准备知识库文档并保存到本地
content = """
        The secret of red is red_000000.
        The secret of green is green_000111.
        The secret of blue is blue_000222.
        The secret of yellow is yellow_000333.
"""

knowledgebase_file = "/tmp/knowledgebase.md"
with open(knowledgebase_file, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Knowledgebase file path: {knowledgebase_file}")

from veadk import Agent, Runner
from veadk.knowledgebase.knowledgebase import KnowledgeBase
from veadk.memory.short_term_memory import ShortTermMemory

app_name = "veadk_playground_app"
user_id = "veadk_playground_user"
session_id = "veadk_playground_session"


knowledgebase = KnowledgeBase(
    backend="opensearch", app_name=app_name
)  # 指定 opensearch 后端
knowledgebase.add_from_files(files=[knowledgebase_file])

agent = Agent(knowledgebase=knowledgebase)

runner = Runner(
    agent=agent,
    short_term_memory=ShortTermMemory(),
    app_name=app_name,
    user_id=user_id,
)


async def main():
    response = await runner.run(
        messages="Tell me the secret of green.", session_id=session_id
    )
    print(response)
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
