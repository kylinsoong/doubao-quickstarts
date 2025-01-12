FROM python:3.9-slim

WORKDIR /app

ADD main.py /app

RUN pip3 install 'confluent-kafka' && pip3 install --upgrade 'volcengine-python-sdk[ark]'

ENV PUB_SUB_EP=na
ENV PUB_SUB_TOPIC=na
ENV PUB_SUB_TOPIC_RRSULT=na
ENV ARK_API_ENGPOINT_ID=na
ENV LLM_VISION_BATCH_SIZE=10

CMD ["python3", "main.py"]
