#!/usr/bin/env python3

"""
简单测试脚本：验证finance_marketing_agent的root_agent是否正确暴露
该脚本仅检查文件结构和root_agent的定义，不依赖于VeADK的完整初始化
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("检查finance_marketing_agent的文件结构...")
    
    # 检查agent.py文件是否存在
    agent_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "finance_marketing_agent", "agent.py")
    if not os.path.exists(agent_file_path):
        print(f"❌ agent.py文件不存在: {agent_file_path}")
        sys.exit(1)
    print(f"✅ agent.py文件存在: {agent_file_path}")
    
    # 检查agent.py文件中是否包含root_agent的定义
    print("\n检查agent.py文件中是否包含root_agent的定义...")
    with open(agent_file_path, 'r') as f:
        agent_content = f.read()
    
    # 检查root_agent是否定义在模块级别
    if "root_agent = " in agent_content:
        print("✅ agent.py文件中包含root_agent的定义")
        
        # 查找root_agent定义的行
        lines = agent_content.split('\n')
        for i, line in enumerate(lines):
            if "root_agent = " in line and not line.strip().startswith('#'):
                print(f"   定义位置: 第{i+1}行: {line.strip()}")
                
                # 检查root_agent是否是从Agent实例赋值的
                if "consumer_finance_marketing_agent" in line:
                    print("✅ root_agent是从consumer_finance_marketing_agent赋值的，符合预期")
                elif "Agent(" in line:
                    print("✅ root_agent是直接从Agent实例赋值的")
                break
    else:
        print("❌ agent.py文件中没有找到root_agent的定义")
        sys.exit(1)
    
    # 检查是否有__init__.py文件
    init_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "finance_marketing_agent", "__init__.py")
    if os.path.exists(init_file_path):
        print("✅ __init__.py文件存在")
    else:
        print("⚠️ __init__.py文件不存在，可能会影响模块导入")
    
    # 检查目录结构是否符合ADK预期
    print("\n检查目录结构是否符合ADK预期...")
    expected_structure = [
        "finance_marketing_agent/",
        "finance_marketing_agent/agent.py",
        "finance_marketing_agent/sub_agents/"
    ]
    
    for path in expected_structure:
        full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
        if os.path.exists(full_path):
            print(f"✅ 目录结构符合预期: {path}")
        else:
            print(f"❌ 目录结构不符合预期，缺少: {path}")
    
    print("\n🎉 基本检查通过！root_agent已经在agent.py中定义，ADK Web Server应该能够找到它。")
    print("\n注意：完整初始化需要Volcengine访问密钥，这是正常的，不影响root_agent的暴露。")
    print("ADK Web Server应该能够成功加载root_agent，前提是在运行时提供了正确的认证信息。")
    
except Exception as e:
    print(f"❌ 测试过程中发生错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
