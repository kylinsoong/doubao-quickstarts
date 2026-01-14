import os
from pydantic_settings import BaseSettings
from typing import Optional


class AppConfig(BaseSettings):
    """应用程序配置"""
    app_name: str = "finance_marketing_agent"
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False


class AgentConfig(BaseSettings):
    main_agent_name: str = "finance_marketing_agent"
    main_agent_description: str = "金融营销助手主智能体，能够根据用户意图选择合适的子智能体执行任务"
    sequential_agent_name: str = "sequential_service_agent"
    sequential_agent_description: str = "根据用户需求，逐步执行工作流，生成最佳回复结果"


class KnowledgeServiceConfig(BaseSettings):
    """知识服务配置"""
    domain: str = "api-knowledgebase.mlp.cn-beijing.volces.com"
    api_key: str = os.getenv("VIKING_SERVICE_API_KEY", "")
    resource_id: str = os.getenv("VIKING_SERVICE_RESOURCE_ID", "")
    timeout: int = 30


class ImageGenerateConfig(BaseSettings):
    """图片生成配置"""
    default_size: str = "1024x1024"
    max_retries: int = 3
    timeout: int = 60


class LogConfig(BaseSettings):
    """日志配置"""
    level: str = os.getenv("LOG_LEVEL", "INFO")
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file: Optional[str] = None


class Config(BaseSettings):
    """主配置类"""
    app: AppConfig = AppConfig()
    agent: AgentConfig = AgentConfig()
    knowledge_service: KnowledgeServiceConfig = KnowledgeServiceConfig()
    image_generate: ImageGenerateConfig = ImageGenerateConfig()
    log: LogConfig = LogConfig()


# 创建全局配置实例
config = Config()
