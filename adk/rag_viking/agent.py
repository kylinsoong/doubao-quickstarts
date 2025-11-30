import os
import requests

# 准备知识库文档并保存到本地
pdf_url = "https://arxiv.org/pdf/1706.03762"
pdf_path = "/tmp/knowledgebase.pdf"
resp = requests.get(pdf_url)
with open(pdf_path, "wb") as f:
    f.write(resp.content)

print(f"Knowledgebase file path: {pdf_path}")

from veadk import Agent
from veadk.knowledgebase.knowledgebase import KnowledgeBase
from veadk.memory.short_term_memory import ShortTermMemory

app_name = "veadk_playground_app"
user_id = "veadk_playground_user"
session_id = "veadk_playground_session"

knowledgebase = KnowledgeBase(backend="viking", app_name=app_name)  # 指定 viking 后端

knowledgebase.add_from_files(files=[pdf_path])  # 直接添加文档，无需手动切片

agent = Agent(knowledgebase=knowledgebase)

root_agent = agent