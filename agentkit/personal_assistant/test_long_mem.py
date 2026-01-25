# 参考如下 memory 示例集成代码，修改 agent 代码
import asyncio
import os

from veadk import Agent, Runner
from veadk.memory.long_term_memory import LongTermMemory
from dotenv import load_dotenv

load_dotenv()

collection_name = os.getenv("DATABASE_VIKINGMEM_COLLECTION")
if not collection_name:
    raise ValueError("DATABASE_VIKINGMEM_COLLECTION environment variable is not set")

long_term_memory = LongTermMemory(backend="viking_mem", index=collection_name)

# Replace the following from your own user & session management system
app_name = "ltm_demo"
user_id = "temp_user"

teaching_session_id = "teaching_session"
student_session_id = "student_session"

agent = Agent(long_term_memory=long_term_memory)

runner = Runner(
    agent=agent,
    app_name=app_name,
    user_id=user_id,
)

teaching_prompt = "My secret is 0xabcd"
asyncio.run(runner.run(messages=teaching_prompt, session_id=teaching_session_id))

# save the teaching prompt and answer in long term memory
asyncio.run(runner.save_session_to_long_term_memory(session_id=teaching_session_id, user_id=user_id))

# now, let's validate this in a new session, with the same user_id configured in the Runner
student_prompt = "What is my secret?"
response = asyncio.run(
    runner.run(messages=student_prompt, session_id=student_session_id)
)
print(response)
