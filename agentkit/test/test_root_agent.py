#!/usr/bin/env python3

"""
测试脚本：验证finance_marketing_agent的root_agent是否正确暴露
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("尝试导入finance_marketing_agent的root_agent...")
    
    # 尝试直接导入root_agent（ADK Web Server使用的方式）
    from finance_marketing_agent.agent import root_agent
    
    print("✅ 成功导入root_agent!")
    print(f"root_agent名称: {root_agent.name}")
    print(f"root_agent描述: {root_agent.description}")
    print(f"root_agent类型: {type(root_agent)}")
    print(f"root_agent是否有子智能体: {hasattr(root_agent, 'sub_agents') and len(root_agent.sub_agents) > 0}")
    
    # 尝试导入主智能体
    from finance_marketing_agent.agent import consumer_finance_marketing_agent
    print(f"\n✅ 成功导入consumer_finance_marketing_agent!")
    print(f"主智能体名称: {consumer_finance_marketing_agent.name}")
    
    # 验证root_agent和主智能体是否是同一个对象
    if root_agent is consumer_finance_marketing_agent:
        print("✅ root_agent和主智能体是同一个对象，符合预期！")
    else:
        print("❌ root_agent和主智能体不是同一个对象，可能存在问题！")
    
    print("\n🎉 测试通过！root_agent已经正确暴露，可以被ADK Web Server访问。")
    
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print("请检查root_agent是否正确暴露在finance_marketing_agent.agent模块中。")
    sys.exit(1)
except Exception as e:
    print(f"❌ 测试过程中发生错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
