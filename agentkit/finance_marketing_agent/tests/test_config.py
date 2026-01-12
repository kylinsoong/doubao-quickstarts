import os
import pytest
from config import Config, AppConfig, AgentConfig, KnowledgeServiceConfig, ImageGenerateConfig, LogConfig


def test_app_config_defaults():
    """测试应用配置默认值"""
    app_config = AppConfig()
    assert app_config.app_name == "consumer_finance_marketing_agent"
    assert app_config.host == "0.0.0.0"
    assert app_config.port == 8000
    assert app_config.debug is False


def test_agent_config_defaults():
    """测试智能体配置默认值"""
    agent_config = AgentConfig()
    assert agent_config.main_agent_name == "consumer_finance_marketing_agent"
    assert "消费金融营销助手" in agent_config.main_agent_description
    assert agent_config.sequential_agent_name == "sequential_service_agent"
    assert "逐步执行工作流" in agent_config.sequential_agent_description


def test_knowledge_service_config_defaults():
    """测试知识服务配置默认值"""
    knowledge_config = KnowledgeServiceConfig()
    assert knowledge_config.domain == "api-knowledgebase.mlp.cn-beijing.volces.com"
    assert knowledge_config.timeout == 30


def test_image_generate_config_defaults():
    """测试图片生成配置默认值"""
    image_config = ImageGenerateConfig()
    assert image_config.default_size == "1024x1024"
    assert image_config.max_retries == 3
    assert image_config.timeout == 60


def test_log_config_defaults():
    """测试日志配置默认值"""
    log_config = LogConfig()
    assert log_config.level == "INFO"
    assert log_config.format == "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    assert log_config.file is None


def test_config_integration():
    """测试配置集成"""
    config = Config()
    assert isinstance(config.app, AppConfig)
    assert isinstance(config.agent, AgentConfig)
    assert isinstance(config.knowledge_service, KnowledgeServiceConfig)
    assert isinstance(config.image_generate, ImageGenerateConfig)
    assert isinstance(config.log, LogConfig)


def test_config_from_env(monkeypatch):
    """测试从环境变量加载配置"""
    # 设置环境变量
    monkeypatch.setenv("APP_NAME", "test_app")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    
    # 创建配置实例
    config = Config()
    
    # 验证配置是否从环境变量加载
    assert config.app.app_name == "test_app"
    assert config.log.level == "DEBUG"


def test_config_override():
    """测试配置覆盖"""
    # 创建自定义配置
    custom_config = Config(
        app=AppConfig(debug=True),
        log=LogConfig(level="DEBUG")
    )
    
    # 验证配置是否被正确覆盖
    assert custom_config.app.debug is True
    assert custom_config.log.level == "DEBUG"
