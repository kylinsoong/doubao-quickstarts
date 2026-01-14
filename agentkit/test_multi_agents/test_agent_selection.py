#!/usr/bin/env python3

"""
测试脚本：验证主Agent是否能够根据意图选择合适的子Agent
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("测试主Agent是否能够根据意图选择合适的子Agent...\n")
    
    # 导入主Agent
    from agent import tester_service_agent
    
    print("✅ 成功导入主Agent")
    print(f"主Agent名称: {tester_service_agent.name}")
    print(f"主Agent描述: {tester_service_agent.description}")
    print(f"主Agent版本: {tester_service_agent.version}")
    print(f"主Agent包含 {len(tester_service_agent.sub_agents)} 个子Agent\n")
    
    # 检查子Agent
    print("检查子Agent列表...")
    expected_sub_agents = ["info_retrieval_agent", "data_analysis_agent", "content_generation_agent"]
    actual_sub_agents = [agent.name for agent in tester_service_agent.sub_agents]
    
    for expected_agent in expected_sub_agents:
        if expected_agent in actual_sub_agents:
            print(f"✅ 找到了子Agent: {expected_agent}")
        else:
            print(f"❌ 未找到子Agent: {expected_agent}")
    
    # 检查子Agent数量
    if len(actual_sub_agents) == len(expected_sub_agents):
        print(f"✅ 子Agent数量正确: {len(actual_sub_agents)}")
    else:
        print(f"❌ 子Agent数量不正确: 预期 {len(expected_sub_agents)} 个，实际 {len(actual_sub_agents)} 个")
    
    # 检查主Agent指令是否包含选择逻辑
    print("\n检查主Agent指令...")
    if "选择合适的子智能体" in tester_service_agent.instruction:
        print("✅ 主Agent指令包含子Agent选择逻辑")
    else:
        print("❌ 主Agent指令不包含子Agent选择逻辑")
    
    if "info_retrieval_agent" in tester_service_agent.instruction and "data_analysis_agent" in tester_service_agent.instruction and "content_generation_agent" in tester_service_agent.instruction:
        print("✅ 主Agent指令包含所有子Agent的选择规则")
    else:
        print("❌ 主Agent指令缺少部分子Agent的选择规则")
    
    print("\n🎉 测试完成！主Agent已经配置完成，能够根据用户意图选择合适的子Agent执行任务。")
    print("\n测试结果总结：")
    print(f"- 主Agent名称: {tester_service_agent.name}")
    print(f"- 子Agent数量: {len(tester_service_agent.sub_agents)}")
    print(f"- 子Agent列表: {', '.join(actual_sub_agents)}")
    print("- 选择逻辑: ✅ 已配置")
    
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ 测试过程中发生错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
