import os
import sys
import logging
from logging.handlers import RotatingFileHandler

from agentkit.apps import AgentkitAgentServerApp
from veadk import Agent, Runner
from veadk.memory.short_term_memory import ShortTermMemory


# Add current directory to Python path to support sub_agents imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入配置和提示词
from config import config
from prompts import CONSUMER_FINANCE_MARKETING_AGENT_PROMPT
from sub_agents.sequential_agent import sequential_service_agent


# 配置日志
logging.basicConfig(
    level=getattr(logging, config.log.level.upper()),
    format=config.log.format,
    handlers=[
        logging.StreamHandler(sys.stdout),
        RotatingFileHandler(
            config.log.file or f"{config.app.app_name}.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
    ]
)

logger = logging.getLogger(__name__)


# 初始化短期记忆
short_term_memory = ShortTermMemory(
    backend="local"
)
logger.info("短期记忆初始化成功")

# 创建主智能体
finance_marketing_agent = Agent(
    name=config.agent.main_agent_name,
    description=config.agent.main_agent_description,
    instruction=CONSUMER_FINANCE_MARKETING_AGENT_PROMPT,
    sub_agents=[sequential_service_agent],
)
logger.info(f"主智能体 {config.agent.main_agent_name} 初始化成功")

# 设置根智能体（模块级别，供ADK Web Server使用）
root_agent = finance_marketing_agent
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
        logger.info(f"启动 {config.app.app_name} 服务...")
        agent_server_app = init_agent()
        agent_server_app.run(host=config.app.host, port=config.app.port)
        logger.info(f"{config.app.app_name} 服务已启动，监听地址: {config.app.host}:{config.app.port}")
    except KeyboardInterrupt:
        logger.info(f"{config.app.app_name} 服务已被用户中断")
    except Exception as e:
        logger.error(f"{config.app.app_name} 服务启动失败: {str(e)}", exc_info=True)
        sys.exit(1)
