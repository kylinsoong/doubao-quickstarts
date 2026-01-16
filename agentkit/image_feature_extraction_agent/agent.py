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
import sys
import os

from veadk import Agent, Runner
from agentkit.apps import AgentkitAgentServerApp
from veadk.memory.short_term_memory import ShortTermMemory

# 初始化日志
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 添加上级目录到 Python 路径，以便导入 prompt 模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入提示词
try:
    from prompt import IMAGE_FEATURE_EXTRACTION_PROMPT
except ImportError as e:
    logger.error(f"导入 prompt 模块失败: {e}")
    raise

# 初始化短期记忆
short_term_memory = ShortTermMemory(
    backend="local"
)
logger.info("短期记忆初始化成功")

# 智能体配置
agent_name = "image_feature_extraction_agent"
description = "图片特征提取智能体，用于分析图片并提取其关键特征"
system_prompt = IMAGE_FEATURE_EXTRACTION_PROMPT
tools = []

# 创建智能体
image_feature_extraction_agent = Agent(
    name=agent_name,
    description=description,
    instruction=system_prompt,
    tools=tools,
)
logger.info(f"智能体 {agent_name} 初始化成功")

# 设置根智能体（模块级别，供ADK Web Server使用）
root_agent = image_feature_extraction_agent
logger.info("根智能体初始化成功")

# 创建运行器
runner = Runner(agent=root_agent)
logger.info("运行器初始化成功")


def init_agent():
    """初始化智能体应用服务器"""
    try:
        # 创建应用服务器
        agent_server_app = AgentkitAgentServerApp(
            agent=root_agent,
            short_term_memory=short_term_memory,
        )
        logger.info("应用服务器初始化成功")

        return agent_server_app
    except Exception as e:
        logger.error(f"智能体应用服务器初始化失败: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    try:
        logger.info(f"启动 {agent_name} 服务...")
        agent_server_app = init_agent()
        agent_server_app.run(host="0.0.0.0", port=8000)
        logger.info(f"{agent_name} 服务已启动，监听地址: 0.0.0.0:8000")
    except KeyboardInterrupt:
        logger.info(f"{agent_name} 服务已被用户中断")
    except Exception as e:
        logger.error(f"{agent_name} 服务启动失败: {str(e)}", exc_info=True)
        sys.exit(1)
