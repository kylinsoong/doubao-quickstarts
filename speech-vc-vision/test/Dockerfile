FROM python:3.9-slim

WORKDIR /app

ADD main.py /app

RUN pip3 install 'confluent-kafka'

ENV PUB_SUB_EP=na
ENV PUB_SUB_TOPIC_TEST=na

CMD ["python3", "main.py"]
