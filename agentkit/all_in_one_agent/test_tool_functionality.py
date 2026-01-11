#!/usr/bin/env python3

# 测试knowledge_service_search工具的实际功能

from custom_tools import knowledge_service_search
import os

print("测试knowledge_service_search工具的功能")
print("="*50)

# 测试1: 使用默认参数
print("\n测试1: 使用默认参数")
print("调用: knowledge_service_search()")
try:
    result = knowledge_service_search()
    print(f"结果: {result}")
    print(f"类型: {type(result)}")
    print(f"图片链接数量: {len(result)}")
    if len(result) > 0:
        print("第一个图片链接:", result[0])
except Exception as e:
    print(f"错误: {e}")

# 测试2: 提供自定义查询
print("\n" + "="*50)
print("测试2: 提供自定义查询")
custom_query = "ByteDance 办公室"
print(f"调用: knowledge_service_search(query='{custom_query}')")
try:
    result = knowledge_service_search(query=custom_query)
    print(f"结果: {result}")
    print(f"图片链接数量: {len(result)}")
except Exception as e:
    print(f"错误: {e}")



print("\n" + "="*50)
print("功能测试完成！")