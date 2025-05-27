import os
import argparse
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

prompt_template = """
根据如下数据, 生成 echarts {{type}} 图形代码 

<数据>
{{data}}
</数据>

要求：
1. 生成代码格式为 html, 可以直接浏览器渲染显示
2. 界面可以显示多个页面，例如可以基于同样数据生成不同类型的图
3. 原始数据需要表格化展现，可增加趋势变化列等
4. 生成的图像颜色亮丽，可以有渐变色
5. 处理图表和原始数据外，还需要增加数据分析与建议，结合图表和原始数据，总结展示
6. 只生成代码，不对代码做任何解释
"""

# Create an argument parser
parser = argparse.ArgumentParser(description='Generate ECharts code based on data and chart type.')

# Add an argument for the chart type
parser.add_argument('--type', choices=['bar', 'line', 'pie', 'radar'], required=True,
                    help='Select the chart type (bar/line/pie/radar).')

# Add an argument for the data file
parser.add_argument('--data_file', required=True, help='Path to the file containing data.')

# Parse the arguments
args = parser.parse_args()

# Read data from the file
try:
    with open(args.data_file, 'r') as file:
        data = file.read()
except FileNotFoundError:
    print(f"Error: The file {args.data_file} was not found.")
    exit(1)

# Replace the variables in the template
prompt = prompt_template.replace("{{type}}", args.type).replace("{{data}}", data)

print(prompt)

# Call the API to generate code
client = Ark(api_key=API_KEY)
completion = client.chat.completions.create(
    model=API_EP_ID,
    messages=[
        {"role": "user", "content": prompt}
    ],
    max_tokens=16000,
    temperature=0.1
)

# Output the generated code

with open("output.html", "w", encoding="utf-8") as file:
    file.write(completion.choices[0].message.content)

print("HTML file created successfully.")
