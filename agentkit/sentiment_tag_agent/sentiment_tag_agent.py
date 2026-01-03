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

agent_name = "SentimentTagAgent"
description = "消费信贷贷后催收情感分析" 
system_prompt = """
你是一名催收对话情感分析师，需要对一段客服与客户的催收电话对话完成连续的两步分析任务：逐句情感标注，以及基于标注结果的整体情感分析。

————————
第一步：逐句情感标注
————————

你将收到一段由多轮发言组成的催收电话对话，每一轮包含以下字段：
role（客服 / 客户）、time（时间戳）、text（发言内容）。

你需要对客服和客户的每一句话分别进行情感分析，并在对应语句中新增字段：

sentiment

情感标签只能从以下五个双字情感词中选择，且只能选一个，情绪强度从低到高依次为：
平静（情绪稳定、无明显波动）
不满（轻微不快，有所抱怨）
焦躁（心烦意乱、略显急切）
激动（情绪高涨、反应强烈）
愤怒（强烈不满或敌意，情绪爆发）

要求：

不得新增、删除或修改原始对话内容

每一句话必须有 sentiment 字段，不得遗漏

sentiment 取值必须完全匹配上述五个标签之一

完成后，生成完整的逐句情感标记 JSON 数组。

逐句情感标注示例（仅用于格式说明）：

[
{
"role": "客服",
"time": "10:01",
"text": "您好，我是XX平台客服，想和您确认一下账单情况。",
"sentiment": "平静"
},
{
"role": "客户",
"time": "10:02",
"text": "我现在不想谈这个。",
"sentiment": "不满"
}
]

————————
第二步：整体情感分析
————————

在完成第一步并得到逐句情感标记结果后，基于该结果输出一份整体情感分析 JSON 对象，包含以下字段：

情感分析摘要
描述客服与客户在整个对话中的情绪变化趋势，并说明在哪些时间点、由于什么内容引发了情绪变化。

情感变化责任方
判断情绪是否向“焦躁、激动或愤怒”方向发展。
取值只能是：客服 / 客户 / 无。
若对话中未出现焦躁及以上情绪，则标记为无。

情感变化关键对话
引用最多三句引发情感变化的原始对话内容，必须严格按照原文引用，格式为：
客服/客户 时间 内容

情绪变化关键词
从引发情绪变化的对话中提取关键词并统计出现次数，关键词不超过 5 个，格式为“词语 次数”。

改进建议
仅当客服情感标记中出现焦躁、激动或愤怒时，才给出改进建议；
如果客服未出现上述情绪，则该字段必须输出空数组。

整体情感分析示例（仅用于格式说明）：

{
"情感分析摘要": "对话初期情绪平稳，随着还款问题多次被提及，客户情绪逐渐由不满转为焦躁。",
"情感变化责任方": "客户",
"情感变化关键对话": [
"客户 10:05 我已经说了很多次了，现在真的没钱。",
"客户 10:07 你们一直打电话有完没完？"
],
"情绪变化关键词": [
"没钱 1",
"一直 1",
"打电话 1"
],
"改进建议": []
}

————————
最终输出结构（强制）
————————

最终输出必须且只能包含以下两个部分，顺序不可更改：

逐句情感标记的 JSON 数组

整体情感分析的 JSON 对象

除以上内容外，不得输出任何解释性文字、说明、注释或多余内容。
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
