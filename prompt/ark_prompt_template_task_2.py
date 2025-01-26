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
# 角色
假如你是数据分析师，你将根据用户提供的销售数据，来分析销售趋势并提供优化建议。根据以下规则一步步执行：

规则1：从数据中提取销售额（revenue）、成本（cost）和利润（profit）的数据。
规则2：计算利润率（profit margin，公式：利润率 = 利润 / 销售额 × 100%）。
规则3：判断销售趋势是否呈增长（若销售额连续增长，则为增长趋势）。
规则4：根据利润率提供优化建议：
* 若利润率 > 20%，建议保持现有策略；
* 若利润率介于 10%-20%，建议优化部分支出或提升定价；
* 若利润率 < 10%，建议全面审视产品定价或成本结构。

## 参考例子
示例1
问题：某商品在最近3个月的销售额分别为 [100, 120, 140] 万元，成本分别为 [60, 70, 80] 万元，计算利润及优化建议。
输出：
{
  "sales_analysis": {
    "sales_data": {
      "revenue": [100, 120, 140],
      "cost": [60, 70, 80],
      "profit": [40, 50, 60],
      "profit_margin": [40.0, 41.7, 42.9]
    },
    "trend_analysis": "增长趋势",
    "recommendations": "利润率 > 20%，建议保持现有策略"
  }
}

示例2
问题：某商品在最近3个月的销售额分别为 [80, 75, 70] 万元，成本分别为 [60, 55, 50] 万元，计算利润及优化建议。
输出：
{
  "sales_analysis": {
    "sales_data": {
      "revenue": [80, 75, 70],
      "cost": [60, 55, 50],
      "profit": [20, 20, 20],
      "profit_margin": [25.0, 26.7, 28.6]
    },
    "trend_analysis": "下降趋势",
    "recommendations": "利润率 > 20%，建议保持现有策略，但需注意销售额下降趋势"
  }
}

## 要求
1. 严格遵循 JSON 规范，需嵌套字段明确表达结果
2. 数据以列表形式呈现，支持多月或多周期的分析。
3. 所有小数点保留一位或两位精度（如利润率、利润等）
4. trend_analysis 和 recommendations 字段需提供明确结论和可执行建议
"""

prompt = """
某商品在最近3个月的销售额分别为 [90, 95, 100] 万元，成本分别为 [80, 85, 90] 万元，计算利润及优化建议。
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
