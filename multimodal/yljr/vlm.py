import json
import os
from volcenginesdkarkruntime import Ark
import logging
import random
import concurrent.futures

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

models = [os.environ.get("ARK_API_ENGPOINT_ID")] 

def ark_vision_images(item, prompt, temperature):
    messages = [
        {"role": "user", "content": [{"type": "text", "text": prompt}] + [
            {"type": "image_url", "image_url": {"url": url}} for url in item
        ]}
    ]
    try:
        completion = client.chat.completions.create(
            model=random.choice(models),
            messages=messages,
            temperature=temperature
        )
        return completion.choices[0].message.content, completion.usage
    except Exception as e:
        return None

API_KEY = os.environ.get("ARK_API_KEY")

client = Ark(api_key=API_KEY)


prompt = """
分析一组图片，提取图片中标题、检索项、和列字段。

# 说明
1. 标题位于导航栏下面，通常格式是 <标题>  <标题描述>，标题为加粗字体
2. 检索项位于表格列之上，用于查询表格，要求提取所有检索项，以表格方式显示，表格为2列，第一列为序号，第二列为检索项名称
3. 提取所有列字段名称，以表格方式显示，表格为2列，第一列为序号，第二列为列名称

# 输出格式

严格以如下格式输出：

## <图片1名称>

原始图片1 URL, Markdump 格式

### <图片1 提取到的标题>
<标题描述>

### 检索项
<检索项表格>

### 列字段
<列字段表格>

## <图片2名称>

原始图片2 URL, Markdump 格式

### <图片2 提取到标题>
<标题描述>

### 检索项
<检索项表格>

### 列字段
<列字段表格>

// 如果有更多图片，则依次罗列

"""

items = ["https://pub-kylin.tos-cn-beijing.volces.com/yljr/test01.jpg", "https://pub-kylin.tos-cn-beijing.volces.com/yljr/test02.jpg", "https://pub-kylin.tos-cn-beijing.volces.com/yljr/test03.jpg"]

results = ark_vision_images(items, prompt, 0.01)

print(results[0]) 
print()
print(results[1]) 
