FROM python:3.9-slim

WORKDIR /app

RUN mkdir -p /app/keys

COPY private_key.pem /app/keys/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

# 启动命令
CMD ["python", "app.py"]
