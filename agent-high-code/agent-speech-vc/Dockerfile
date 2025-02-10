FROM python:3.9-slim

WORKDIR /app

ADD main.py /app

RUN pip3 install 'confluent-kafka' && pip3 install requests

ENV PUB_SUB_EP=na
ENV PUB_SUB_TOPIC=na
ENV X_API_APPID=na
ENV X_API_TOKEN=na
ENV LLM_SPEECH_THRESHOLD_MS=12000

CMD ["python3", "main.py"]
