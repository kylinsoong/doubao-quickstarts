# 消费金融营销助手 (Finance Marketing Agent)

## 项目概述

消费金融营销助手是一个基于大语言模型的智能代理系统，专注于为金融行业提供自动化营销素材生成服务。该系统通过多智能体协作，实现从需求分析到素材生成的全流程自动化，能够生成高质量、个性化的营销文案、图片和视频，帮助金融机构提升营销效率和效果。

## 系统架构

### 智能体结构

```
+---------------------------------+
| 消费金融营销主智能体             |
| (Finance Marketing Agent)       |
+---------------------------------+
               |
               +------------+----------------+--------------------+
               |            |                |                    |            
               v            v                v                    v            
+---------------+      +-------------+      +-------------+      +-----------------------+
| 文案创作      |      | 图片生成    |      | 视频生成    |      | 图片编辑              |
| (Content Gen) |      | (Image Gen) |      | (Video Gen) |      | (Sequential Agent)    |
                                                                 +------------+----------+
                                                                     |              |
                                                                     v              v
                                                                 +--------------+ +------------+
                                                                 | 查询改写     | | 知识库搜索 |
                                                                 | Query Rewrite| | Search KB  |
                                                                 +--------------+ +------------+
                                                                                 |
                                                                                 v
                                                                           +--------------+
                                                                           | 图片编辑     |
                                                                           | (Image Edit) |
                                                                           +--------------+
                                                                                 |
                                                                                 v
                                                                           +----------------+
                                                                           | 结果评估       |
                                                                           | (Quality Eval) |
                                                                           +----------------+
```

### 核心智能体介绍

#### 1. 主智能体 (Finance Marketing Agent)
- **角色**：智能任务调度员
- **核心功能**：根据用户意图选择合适的子智能体
- **提示词**：`FINANCE_MARKETING_AGENT_PROMPT`
- **选择逻辑**：
  - 营销文案创作 → promotional_text_creation_agent
  - 营销图片创作 → promotional_image_generate_agent
  - 营销视频创作 → promotional_video_creation_agent
  - 图片编辑 → retrive_img_from_kb_generate_new_img_agent

#### 2. 串行控制智能体 (Sequential Service Agent)
- **角色**：串行总控专家
- **核心功能**：按顺序协调图片编辑工作流
- **提示词**：`SEQUENTIAL_SERVICE_AGENT_PROMPT`
- **工作流程**：
  1. 用户信息预处理 → kb_query_rewriting_agent
  2. 知识库搜索 → search_kb_agent
  3. 图片编辑 → edit_image_agent
  4. 结果评估 → quality_control_agent

#### 3. 需求分析智能体 (Query Rewriting Agent)
- **角色**：消费金融营销需求分析师
- **核心功能**：提取知识库查询关键词
- **提示词**：`IMG_KB_QUERY_REWRITING_AGENT_PROMPT`
- **提取规则**：
  - 提取核心主题词
  - 忽略无关修饰词
  - 只提取查询图片部分的关键词

#### 4. 知识库搜索智能体 (Search KB Agent)
- **角色**：专业知识库搜索专家
- **核心功能**：使用 knowledge_service_search 工具查询知识库
- **提示词**：`SEARCH_KB_AGENT_PROMPT`
- **工具调用**：knowledge_service_search

#### 5. 营销文案创作智能体 (Content Generation Agent)
- **角色**：金融科技与消费金融行业专业营销文案专家
- **核心功能**：创作专业、合规、可信的消费金融营销文案
- **提示词**：`PROMOTIONAL_CONTENT_GENERATION_AGENT_PROMPT`
- **合规约束**：
  - 不承诺放款成功率、收益或零风险
  - 不使用“100%通过”“秒批秒放”等表述
  - 强调风控体系和合规运营

#### 6. 营销图片生成智能体 (Image Generation Agent)
- **角色**：金融科技与消费金融行业专业视觉内容生成专家
- **核心功能**：生成合规、专业的营销图片
- **提示词**：`IMAGEOTIONAL_IMAGE_GENERATE_AGENT_PROMPT`
- **生成限制**：
  - 不得暗示放款必过、收益保证或零风险
  - 不得出现具体金额、利率等承诺性信息
  - 风格应体现可信、安全、稳健与科技感

#### 7. 营销视频生成智能体 (Video Generation Agent)
- **角色**：金融科技与消费金融行业专业视频内容生成专家
- **核心功能**：生成合规、专业的营销视频
- **提示词**：`PROMOTIONAL_VEDIO_GENERATION_AGENT_PROMPT`
- **生成限制**：
  - 不得暗示放款必过、收益保证或零风险
  - 不得出现具体金额、利率等承诺性信息
  - 风格应体现可信、安全、稳健与科技感

#### 8. 图片编辑智能体 (Edit Image Agent)
- **角色**：消费金融营销图片生成专家
- **核心功能**：根据底图和设计要求生成高质量营销素材
- **提示词**：`EDIT_IMAGE_AGENT_PROMPT`
- **生成规则**：
  - 高清分辨率（至少1024x1024）
  - 文字清晰可读，排版美观
  - 符合金融行业规范和品牌要求
  - 设计风格匹配目标受众

## 工作流程

### 1. 营销文案生成流程

1. **用户输入**：用户提出营销文案需求
2. **主智能体**：接收需求，判断意图
3. **营销文案创作智能体**：生成专业、合规的营销文案
4. **质量控制**：评估生成文案质量
5. **输出结果**：返回生成的营销文案

### 2. 营销图片生成流程

1. **用户输入**：用户提出营销图片生成需求
2. **主智能体**：接收需求，判断意图
3. **图片生成智能体**：直接生成营销图片
4. **质量控制**：评估生成图片质量
5. **输出结果**：返回生成的营销图片链接

### 3. 营销视频生成流程

1. **用户输入**：用户提出营销视频生成需求
2. **主智能体**：接收需求，判断意图
3. **视频生成智能体**：直接生成营销视频
4. **质量控制**：评估生成视频质量
5. **输出结果**：返回生成的营销视频链接

### 4. 图片编辑流程

1. **用户输入**：用户提出基于已有素材生成新图的需求
2. **主智能体**：接收需求，判断意图，选择图片编辑工作流
3. **串行控制智能体**：协调图片编辑工作流
4. **需求分析智能体**：提取查询关键词
5. **知识库搜索智能体**：查询相关图片素材
6. **图片编辑智能体**：基于底图生成最终营销图片
7. **结果评估智能体**：评估生成图片质量
8. **输出结果**：返回生成的营销图片链接

## 快速开始

### 环境要求

- Python 3.12+
- VeADK (Volcengine Agent Development Kit)
- Volcengine API 密钥

### 安装步骤

1. **克隆项目代码**

```bash
git clone <repository-url>
cd finance_marketing_agent
```

2. **安装依赖**

```bash
pip install -r requirements.txt
```

3. **配置环境变量**

创建 `.env` 文件，配置必要的环境变量：

```env
# 知识服务配置
VIKING_SERVICE_API_KEY=your-api-key
VIKING_SERVICE_RESOURCE_ID=your-resource-id

# 日志配置
LOG_LEVEL=INFO

# 服务配置
HOST=0.0.0.0
PORT=8000
```

### 运行服务

#### 本地运行

```bash
python agent.py
```

#### Docker 运行

```bash
# 构建镜像
docker build -t finance-marketing-agent .

# 运行容器
docker run -p 8000:8000 --env-file .env finance-marketing-agent
```

## 配置说明

### 配置文件结构

```python
# config.py
class AppConfig(BaseSettings):
    """应用程序配置"""
    app_name: str = "consumer_finance_marketing_agent"
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False

class AgentConfig(BaseSettings):
    """智能体配置"""
    main_agent_name: str = "consumer_finance_marketing_agent"
    main_agent_description: str = "消费金融营销助手，根据用户问题生成相应的营销素材"
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
```

### 配置优先级

1. **环境变量**：优先级最高，会覆盖配置文件中的默认值
2. **配置文件**：项目中的 `config.py` 文件
3. **默认值**：配置类中定义的默认值

## 开发指南

### 项目结构

```
finance_marketing_agent/
├── agent.py              # 主程序入口
├── config.py             # 配置管理
├── prompts.py            # 智能体提示词
├── quality_control.py    # 质量控制模块
├── requirements.txt      # 依赖声明
├── Dockerfile            # Docker构建文件
├── sub_agents/           # 子智能体目录
│   ├── pre_process.py    # 需求分析智能体
│   ├── search_kb.py      # 知识库搜索智能体
│   ├── edit_image.py     # 图片生成智能体
│   └── sequential_agent.py # 串行控制智能体
└── tests/                # 测试目录
    ├── test_config.py    # 配置测试
    └── test_quality_control.py  # 质量控制测试
```

### 智能体开发流程

1. **定义提示词**：在 `prompts.py` 中定义智能体的提示词
2. **创建智能体**：在 `sub_agents/` 目录下创建智能体文件
3. **注册智能体**：在 `sequential_agent.py` 中添加智能体到工作流
4. **测试智能体**：编写测试用例验证智能体功能
5. **部署运行**：部署到生产环境并监控运行情况

### 提示词设计原则

1. **角色明确**：清晰定义智能体的角色和职责
2. **规则明确**：提供明确的决策规则和执行步骤
3. **示例丰富**：提供多个输入输出示例
4. **合规约束**：明确金融行业的合规要求
5. **输出格式**：定义清晰的输出格式

## 监控与日志

### 日志配置

系统默认只输出日志到控制台，日志级别为 INFO。可以通过环境变量 `LOG_LEVEL` 调整日志级别，支持 DEBUG、INFO、WARNING、ERROR、CRITICAL 五个级别。

### 日志格式

```
2026-01-15 10:00:00,000 - root - INFO - 服务启动成功
2026-01-15 10:00:10,000 - root - DEBUG - 智能体开始处理请求
2026-01-15 10:00:20,000 - root - INFO - 营销素材生成成功，质量评分：85.5
```

## 安全性

- **API密钥管理**：通过环境变量安全管理API密钥
- **输入验证**：对用户输入进行严格验证，防止恶意输入
- **输出过滤**：对生成的营销素材进行合规性检查
- **访问控制**：支持基于角色的访问控制
- **合规约束**：严格遵守金融行业监管要求

## 贡献指南

欢迎参与消费金融营销助手的开发和改进！

### 开发流程

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/your-feature`)
3. 提交代码 (`git commit -m 'Add your feature'`)
4. 推送到分支 (`git push origin feature/your-feature`)
5. 创建 Pull Request

### 代码规范

- 遵循 PEP 8 代码规范
- 使用类型注解
- 添加详细的文档注释
- 编写单元测试

## 许可证

本项目采用 MIT 许可证，详见 LICENSE 文件。

## 联系方式

- 项目维护：ByteDance AI Lab
- 技术支持：ai-lab@bytedance.com
- 问题反馈：GitHub Issues

## 版本历史

### v1.0.0 (2026-01-15)

- ✨ 初始版本发布
- 🎯 支持信用卡、贷款等金融产品的营销素材生成
- 📊 集成专业金融知识库
- 🎨 实现高质量营销图片生成
- 📝 支持专业营销文案生成
- 🔍 添加质量控制机制

## 未来规划

- 📱 支持移动端营销素材生成
- 📹 支持营销视频自动生成
- 📊 支持营销效果数据分析
- 🔄 支持持续学习和模型优化
- 🌍 支持多语言和多地区营销需求

---

**消费金融营销助手** - 让金融营销更智能、更高效！ 🚀
