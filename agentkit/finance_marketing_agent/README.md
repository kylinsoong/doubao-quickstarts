# 消费金融营销助手 (Finance Marketing Agent)

## 项目简介

消费金融营销助手是一个基于大语言模型的智能代理系统，能够根据用户需求生成高质量的消费金融营销素材。该系统通过多智能体协作，实现从需求分析到素材生成的全流程自动化。

## 系统架构

### 智能体结构

```
+--------------------------+
| 主智能体                  |
| (Consumer Finance Agent) |
+------------+-------------+
             |
             v
+--------------------------+
| 串行控制智能体            |
| (Sequential Agent)       |
+------------+-------------+
             |
             +------------+-------------+------------+
             |            |             |            |
             v            v             v            v
+------------+      +------------+      +------------+      +------------+
| 预处理智能体 |      | 知识库搜索 |      | 图片生成   |      | 质量控制   |
| (Pre-Process) |      | (Search KB) |      | (Image Gen) |      | (Quality Ctrl)|      
+------------+      +------------+      +------------+      +------------+
```

### 核心组件

1. **主智能体 (Consumer Finance Agent)**：接收用户需求，协调子智能体工作
2. **串行控制智能体 (Sequential Agent)**：按顺序执行子智能体，确保工作流完整
3. **预处理智能体 (Pre-Process Agent)**：从用户需求中提取关键信息
4. **知识库搜索智能体 (Search KB Agent)**：查询知识库获取相关素材
5. **图片生成智能体 (Image Generate Agent)**：根据底图和要求生成营销图片
6. **质量控制模块 (Quality Control)**：评估和筛选高质量营销素材

## 安装与配置

### 环境要求

- Python 3.12+
- Docker (可选，用于容器化部署)

### 安装步骤

1. 克隆项目代码

```bash
git clone <repository-url>
cd finance_marketing_agent
```

2. 安装依赖

```bash
pip install -r requirements.txt
```

### 配置管理

系统配置通过以下方式管理：

1. **配置文件**：`config.py` 中定义了系统的默认配置
2. **环境变量**：支持通过环境变量覆盖配置
3. **命令行参数**：部分配置支持通过命令行参数调整

### 环境变量

| 变量名 | 描述 | 默认值 |
|--------|------|--------|
| `VIKING_SERVICE_API_KEY` | 知识服务API密钥 | - |
| `VIKING_SERVICE_RESOURCE_ID` | 知识服务资源ID | - |
| `LOG_LEVEL` | 日志级别 | INFO |
| `HOST` | 服务监听地址 | 0.0.0.0 |
| `PORT` | 服务监听端口 | 8000 |

## 使用指南

### 本地运行

```bash
python agent.py
```

### Docker部署

```bash
# 构建镜像
docker build -t finance-marketing-agent .

# 运行容器
docker run -p 8000:8000 --env-file .env finance-marketing-agent
```

### Docker Compose

```bash
docker-compose up -d
```

## API接口

### 健康检查

```
GET /health
```

### 生成营销素材

```
POST /api/v1/generate
Content-Type: application/json

{
  "query": "我需要为我们的信用卡产品生成一组营销图片，主题是'便捷支付'，目标受众是年轻职场人士。"
}
```

## 测试

### 运行单元测试

```bash
python -m pytest tests/ -v
```

### 运行覆盖率测试

```bash
python -m pytest tests/ --cov=. --cov-report=html
```

## 项目结构

```
finance_marketing_agent/
├── agent.py              # 主程序入口
├── config.py             # 配置管理
├── custom_tools.py       # 自定义工具
├── prompts.py            # 智能体提示词
├── quality_control.py    # 质量控制模块
├── requirements.txt      # 依赖声明
├── Dockerfile            # Docker构建文件
├── docker-compose.yml    # Docker Compose配置
├── README.md             # 项目文档
├── sub_agents/           # 子智能体目录
│   ├── __init__.py
│   ├── sequential_agent.py
│   ├── pre_process.py
│   ├── search_kb.py
│   └── generate_image.py
└── tests/                # 测试目录
    ├── __init__.py
    ├── test_config.py
    └── test_quality_control.py
```

## 版本管理

### 智能体版本

| 智能体名称 | 版本 | 描述 |
|------------|------|------|
| pre_process_agent | 1.0.0 | 预处理智能体 |
| search_kb_agent | 1.0.0 | 知识库搜索智能体 |
| generate_image_agent | 1.0.0 | 图片生成智能体 |
| sequential_service_agent | 1.0.0 | 串行控制智能体 |

## 质量控制

系统实现了多层次的质量控制机制：

1. **相关性评估**：评估素材与用户需求的相关性
2. **创意性评估**：评估素材的创意水平
3. **清晰度评估**：评估素材的视觉清晰度
4. **合规性评估**：评估素材是否符合金融行业规范

质量评分范围为0-100分，默认70分以上为高质量素材。

## 监控与日志

系统实现了完善的日志记录机制：

1. **日志级别**：支持DEBUG、INFO、WARNING、ERROR、CRITICAL五个级别
2. **日志格式**：包含时间戳、模块名、级别、消息等信息
3. **日志输出**：同时输出到控制台和文件
4. **日志滚动**：支持按大小滚动，防止日志文件过大

## 安全性

1. **API密钥管理**：通过环境变量安全管理API密钥
2. **输入验证**：对所有输入进行严格验证
3. **错误处理**：实现了完善的错误处理机制，避免敏感信息泄露
4. **日志脱敏**：对日志中的敏感信息进行脱敏处理

## 扩展与定制

### 添加新的智能体

1. 在 `sub_agents/` 目录下创建新的智能体文件
2. 在 `prompts.py` 中定义智能体的提示词
3. 在 `sequential_agent.py` 中添加智能体到工作流

### 扩展工具集

1. 在 `custom_tools.py` 中定义新的工具函数
2. 在对应的智能体文件中注册工具
3. 在 `prompts.py` 中更新智能体提示词

## 最佳实践

1. **明确的需求描述**：提供清晰、具体的营销需求，包括目标受众、主题、风格等
2. **合理的期望设置**：生成高质量的营销素材需要一定时间，建议预留充足时间
3. **定期评估与优化**：定期评估生成结果，根据反馈优化提示词和工作流
4. **结合人工审核**：对于重要的营销活动，建议结合人工审核确保素材质量

## 故障排除

### 常见问题

1. **服务启动失败**
   - 检查API密钥和资源ID是否正确配置
   - 检查端口是否被占用
   - 查看日志文件获取详细错误信息

2. **生成结果不符合预期**
   - 优化提示词，提供更具体的需求描述
   - 检查知识库中是否有相关素材
   - 调整质量控制阈值

3. **性能问题**
   - 优化智能体工作流，减少不必要的步骤
   - 调整日志级别，减少日志输出
   - 考虑使用更强大的硬件资源

## 贡献指南

欢迎提交Issue和Pull Request！

### 提交流程

1. Fork本仓库
2. 创建新的分支
3. 提交代码
4. 运行测试确保代码质量
5. 提交Pull Request

## 许可证

[MIT License](LICENSE)

## 联系方式

如有问题或建议，请通过以下方式联系：

- Email: [your-email@example.com]
- GitHub Issues: [repository-url/issues]
