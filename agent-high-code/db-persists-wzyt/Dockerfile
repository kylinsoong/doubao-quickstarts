FROM python:3.9-slim

WORKDIR /app

ADD app.py /app

RUN pip3 install 'confluent-kafka' && pip3 install 'pymongo'

ENV PUB_SUB_EP=na
ENV PUB_SUB_TOPIC_RRSULT=na
ENV DB_URL=na
ENV DB_NAME=na
ENV DB_TABLE_NAME=na

CMD ["python3", "app.py"]
