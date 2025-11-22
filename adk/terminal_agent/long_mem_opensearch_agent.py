from veadk import Agent, Runner
from veadk.memory.long_term_memory import LongTermMemory
from veadk.memory.short_term_memory import ShortTermMemory
import os
import asyncio

os.environ["MODEL_EMBEDDING_DIM"] = "2560"
# 数据存入向量数据库之前，需要用embedding模型做向量化，这里调用embedding模型时复用agent的api_key
os.environ["MODEL_EMBEDDING_API_KEY"] = os.environ["MODEL_AGENT_API_KEY"]

app_name = "veadk_playground_app_long_term"
user_id = "veadk_playground_user_long_term"

# 初始化一个长期记忆，采用 OpenSearch 向量化存储
# 长期记忆是跨 Session 的
long_term_memory = LongTermMemory(
    backend="opensearch", app_name=app_name
)

agent = Agent(long_term_memory=long_term_memory)

runner = Runner(
    agent=agent,
    app_name=app_name,
    user_id=user_id,
    short_term_memory=ShortTermMemory(),
)

# ===== 插入记忆 =====
session_id_1 = "veadk_playground_session_1"
teaching_prompt = "我上周五购买了一支冰激凌。"

# ===== 检验记忆 =====
session_id_2 = "veadk_playground_session_2"  # 使用一个新的 Session 来检测跨 Session 检索
student_prompt = "我上周五购买了什么? 用中文回答我。"

async def main():
    # ===== 插入记忆 =====
    await runner.run(messages=teaching_prompt, session_id=session_id_1)
    await runner.save_session_to_long_term_memory(
        session_id=session_id_1
    )  # 将 teaching prompt 和智能体回答保存到长期记忆中

    # ===== 检验记忆 =====
    response = await runner.run(messages=student_prompt, session_id=session_id_2)
    print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
