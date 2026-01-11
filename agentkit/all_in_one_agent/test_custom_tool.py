#!/usr/bin/env python3

# 测试自定义工具的导入和使用

# 导入自定义工具
from custom_tools import knowledge_service_search

print("测试knowledge_service_search工具")
print("工具已成功导入")

# 检查工具的基本信息
print(f"工具名称: {knowledge_service_search.__name__}")
print(f"工具文档: {knowledge_service_search.__doc__}")

# 打印工具的签名
import inspect
print(f"工具签名: {inspect.signature(knowledge_service_search)}")

print("\n测试完成，工具已成功创建和导入！")