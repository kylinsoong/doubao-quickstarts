import os
import sys
import termios
from volcenginesdkarkruntime import Ark
from datetime import datetime

def wait_for_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        sys.stdin.read(1)  # 等待按下任意键
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

client = Ark(api_key=API_KEY)

print("start no-streaming request...")
start_time = datetime.now()
completion = client.chat.completions.create(
    model=API_EP_ID,
    messages=[
        {"role": "system", "content": "你是豆包，是由字节跳动开发的 AI 人工智能助手"},
        {"role": "user", "content": "常见的十字花科植物有哪些？"}
    ]
)
print(completion.choices[0].message.content)
end_time = datetime.now()
time_difference = end_time - start_time

print(f"Non-streaming request spending: {time_difference.total_seconds()}")
print()
print("print any key to start streaming request...")
wait_for_key()

stream = client.chat.completions.create(
    model=API_EP_ID,
    messages=[
        {"role": "system", "content": "你是豆包，是由字节跳动开发的 AI 人工智能助手"},
        {"role": "user", "content": "常见的十字花科植物有哪些？"}
    ],
    stream=True
)

for chunk in stream:
    if not chunk.choices:
        continue
    print(chunk.choices[0].delta.content, end="")
print()


