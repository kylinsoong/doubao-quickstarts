import asyncio
import os

from veadk import Agent, Runner
from veadk.memory.long_term_memory import LongTermMemory
from veadk.memory.short_term_memory import ShortTermMemory

os.environ["MODEL_EMBEDDING_DIM"] = "2560"
# 数据存入向量数据库之前，需要用embedding模型做向量化，这里调用embedding模型时复用agent的api_key
os.environ["MODEL_EMBEDDING_API_KEY"] = os.environ["MODEL_AGENT_API_KEY"]

app_name = "veadk_playground_app"
user_id = "veadk_playground_user"

# 初始化一个长期记忆，采用 Viking DB 记忆库
# 长期记忆是跨 Session 的
long_term_memory = LongTermMemory(backend="viking", app_name=app_name)

agent = Agent(long_term_memory=long_term_memory)

runner = Runner(
    agent=agent,
    app_name=app_name,
    user_id=user_id,
    short_term_memory=ShortTermMemory(),
)

# ===== 插入记忆 =====
session_id = "veadk_playground_session"
teaching_prompt = "我上周五购买了一支冰激凌。"

asyncio.run(runner.run(messages=teaching_prompt, session_id=session_id))
asyncio.run(
    runner.save_session_to_long_term_memory(session_id=session_id)
)  # 将 teaching prompt 和智能体回答保存到长期记忆中

# ===== 检验记忆 =====
session_id = "veadk_playground_session_2"  # 使用一个新的 Session 来检测跨 Session 检索
student_prompt = "我上周五购买了什么? 用中文回答我。"

print(f"Note: viking记忆库，在第一次插入记忆的时候，构建索引需要几分钟时间。因此在第一次运行时，有可能会报错 (index not ready]: need a few minutes to build index after add messages for the first time)")
response = asyncio.run(runner.run(messages=student_prompt, session_id=session_id))

print(response)
