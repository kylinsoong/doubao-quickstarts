FROM dify-cn-beijing.cr.volces.com/byteplus/python:3.12-slim

WORKDIR /app

COPY app.py .

RUN pip install --no-cache-dir redis

CMD ["python", "app.py"]
