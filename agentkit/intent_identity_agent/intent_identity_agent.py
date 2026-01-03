# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd. and/or its affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import json

from veadk import Agent, Runner

from agentkit.apps import AgentkitSimpleApp

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


app = AgentkitSimpleApp()

agent_name = "IntentIdentityAgent"
description = "消费信贷贷后催收意图打标智能体" 
system_prompt = """
你是一名专业的客服质检与对话意图分析助手。你的任务是对客服与客户的对话进行意图分析，并以 JSON 结构化形式输出结果。

分析需涵盖以下内容：
1. 客服主要意图：从客服发言中判断其核心目的，若无法判断则标记为“无”。
2. 客服次要意图：除主要意图外的辅助目的，若无法判断则标记为“无”。
3. 客户主要意图：从客户发言中判断其核心诉求，若无法判断则标记为“无”。
4. 关键信息点：能够体现客服主要意图、客服次要意图及客户主要意图的原始话术，需直接引用对话中的原话。
5. 对话主题分布：分析客服主要意图、客服次要意图和客户主要意图在整个对话中所占比例，三者比例之和必须为 100%。
6. 风险评估：
   - 若客服主要意图达成，则风险等级为“低”
   - 若客服主要意图未达成，但次要意图达成，则风险等级为“中”
   - 若客服主要意图和次要意图均未达成，则风险等级为“高”
   风险总结格式为："<风险等级> <原因>"

请严格按照以下 JSON 结构输出分析结果，不要输出任何多余内容：

{
    "客服主要意图": "string",
    "客服次要意图": "string",
    "客户主要意图": "string",
    "风险总结": ["<低/中/高>", "<原因>"],
    "关键信息点": [
        "客服发言",
        "客服发言",
        "客户发言"
    ],
    "对话主题分布": {
        "<客服主要意图>": "<百分比>",
        "<客服次要意图>": "<百分比>",
        "<客户主要意图>": "<百分比>"
    }
}
"""


tools = []

# from veadk.tools.builtin_tools.web_search import web_search
# tools.append(web_search)


agent = Agent(
    name=agent_name,
    description=description,
    instruction=system_prompt,
    tools=tools,
)
runner = Runner(agent=agent)


def safe_to_str(data):
    if isinstance(data, dict):
        return json.dumps(data, ensure_ascii=False)
    return str(data)

@app.entrypoint
async def run(payload: dict, headers: dict) -> str:
    prompt = payload["prompt"]
    user_id = headers["user_id"]
    session_id = headers["session_id"]

    logger.info(
        f"Running agent with prompt: {prompt}, user_id: {user_id}, session_id: {session_id}"
    )
    response = await runner.run(messages=safe_to_str(prompt), user_id=user_id, session_id=session_id)

    logger.info(f"Run response: {response}")
    return safe_to_str(response)


@app.ping
def ping() -> str:
    return "pong!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
