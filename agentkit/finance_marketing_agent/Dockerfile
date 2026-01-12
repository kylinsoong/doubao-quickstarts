# 使用Python 3.12作为基础镜像
#FROM python:3.12-slim
FROM agentkit-cn-beijing.cr.volces.com/base/py-simple:python3.12-bookworm-slim-latest

# 设置工作目录
WORKDIR /app

# 复制requirements.txt文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 设置环境变量
ENV PYTHONPATH=/app
ENV LOG_LEVEL=INFO

# 暴露端口
EXPOSE 8000

# 设置健康检查
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8000/health || exit 1

# 启动应用
CMD ["python", "agent.py"]
#CMD ["python", "-m", "agent"]
