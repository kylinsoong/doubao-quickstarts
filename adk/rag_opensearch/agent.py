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



knowledgebase = KnowledgeBase(
    backend="opensearch", app_name=app_name
)  # 指定 opensearch 后端
knowledgebase.add_from_files(files=[knowledgebase_file])

root_agent = Agent(knowledgebase=knowledgebase)