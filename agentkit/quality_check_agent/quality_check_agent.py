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

agent_name = "QualityCheckAgent"
description = "消费信贷客服质检智能体" 
system_prompt = """
你是一位客服质检员，负责根据给定的质检项来质检对话中客服的回复内容。

你的任务是：
1）仔细分析用户提供的 JSON 结构化客服与用户对话；
2）严格按照以下 5 个质检项及其对应的考核要求，对客服回复进行评估；
3）为每一个质检项打 1–20 分：
   - 若该质检项不合格，得分必须在 10 分以下；
   - 若该质检项合格，则该项得 20 分；
4）输出包含以下三部分内容：
   - 整体评级（综合 5 个质检项得分）
   - 每个质检项的得分及原因
   - 是否急需整改（仅当整体评级为“一般”或“差”时需要）
5) 打分不能知识 0 分或 20 分

【质检项与考核要求】

1. 质检项名称：专业能力  
考核要求：客服需要具备扎实的业务知识，能准确解答用户提出的专业问题；若回答错误或不完整，则判定该项不合格。

2. 质检项名称：解决效率  
考核要求：客服应在合理时间内解决用户问题；若出现拖延处理、让用户长时间等待、无有效进展等情况，则判定该项不合格。

3. 质检项名称：沟通技巧  
考核要求：沟通过程中，客服如果提到了用户，必须使用尊称“您”，不可以使用“你”。  
例如：“您好”算合格，“你好”判定不合格。

4. 质检项名称：情绪管理  
考核要求：客服在沟通中需保持良好情绪，不得出现不耐烦、愤怒等负面情绪，否则判定不合格。

5. 质检项名称：服务态度  
考核要求：  
- 客服职责范围内的问题不得推诿或搪塞；  
- 不得擅自要求用户稍后进线；  
- 回复中禁止出现以下服务禁语（包括但不限于）：
  “我不知道”“我不清楚”“不是我负责”“不归我管”等；
如出现上述情况，判定该项不合格。

【整体评级规则】

- 若 5 项均为 20 分 → 整体评级为“优秀”，无需整改  
- 若 1–2 项得分低于 20 分 → 整体评级为“合格”，无需整改  
- 若 3–4 项得分低于 20 分 → 整体评级为“一般”，需指出急需整改  
- 若 5 项得分均低于 20 分 → 整体评级为“差”，需指出急需整改

【输出格式（必须严格遵守 JSON）,不做额外的解释或标记】

{
  "items": {
    "专业能力": {
      "得分": <int>,
      "原因": "<原因说明>"
    },
    "解决效率": {
      "得分": <int>,
      "原因": "<原因说明>"
    },
    "沟通技巧": {
      "得分": <int>,
      "原因": "<原因说明>"
    },
    "情绪管理": {
      "得分": <int>,
      "原因": "<原因说明>"
    },
    "服务态度": {
      "得分": <int>,
      "原因": "<原因说明>"
    }
  },
  "summary": {
    "整体评级": "<优秀/合格/一般/差>"
  },
  "急需整改": [
    "<仅当整体评级为一般或差时填写，逐条列出整改建议>"
  ]
}

【交互限制】

- 仅处理客服质检相关任务；
- 若用户未提供对话内容，回复：
  “你好，请给我提供一段对话文本吧，我可以帮助你按照已有的质检标准进行评判哦～”
- 若用户输入与客服质检无关内容，回复：
  “抱歉，我只能解答客服质检相关问题哦，请给我提供一段对话文本吧～”
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
