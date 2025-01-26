import os
import json
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

client = Ark(api_key=API_KEY)

TIP = """任务型模版

假如你是{某个角色}，你将根据{上下文信息}，来解决{具体某个任务}。根据以下规则一步步执行：
1.规则1
2.规则2

参考例子：
示例1：
问题：{具体问题}
输出：{该问题的结果}

示例2：
问题：{具体问题}
输出：{该问题的结果}

请回答问题：
问题：{具体问题}
输出：

要求：
1 指定输出格式
2 格式中需要满足的详细规范
"""


system_prompt = """
假如你是财务分析师，你将根据公司提供的季度财务报告，来分析公司的盈利能力。根据以下规则一步步执行：

规则1：从财务报告中提取总收入、总支出和净利润数据。
规则2：计算净利润率（公式：净利润率 = 净利润 / 总收入 × 100%）。
规则3：分析净利润率是否达到行业平均水平（假设行业平均为15%）。

参考例子
示例1：
问题：某公司第一季度总收入为 500 万元，总支出为 420 万元，净利润为 80 万元。请分析公司的盈利能力。
输出：
总收入：500 万元
总支出：420 万元
净利润：80 万元
净利润率：16%
分析：该公司的净利润率高于行业平均水平（15%），表现优异。

示例2：
问题：某公司第二季度总收入为 300 万元，总支出为 270 万元，净利润为 30 万元。请分析公司的盈利能力。
输出：
总收入：300 万元
总支出：270 万元
净利润：30 万元
净利润率：10%
分析：该公司的净利润率低于行业平均水平（15%），需要优化支出或提升收入。

要求：
1. 输出内容需包含：总收入、总支出、净利润、净利润率、分析。
2. 各项内容需按独立条目呈现，层次分明。
3. 所有数据保留整数或小数点后两位（如有必要）。
4. 分析部分需明确与行业平均水平的对比结果，并提供建议或结论。
"""

prompt = """
某公司第三季度总收入为 600 万元，总支出为 510 万元，净利润为 90 万元。请分析公司的盈利能力。
"""

system_message = {
    "role": "system",
    "content": system_prompt
}
user_message = {
    "role": "user",
    "content": prompt
}

messages = [system_message, user_message]

def main():
    print("==>", TIP)
    print("<PROMPT>: ", prompt)
    print("<RESPONSE>:")
    completion = client.chat.completions.create(
        model=API_EP_ID,
        messages=messages
    )

    print(completion.choices[0].message.content)
    print(completion.usage)


if __name__ == "__main__":
    main()
