FROM python:3.9-slim

WORKDIR /app

ADD main.py /app

RUN pip3 install 'confluent-kafka' && pip3 install --upgrade 'volcengine-python-sdk[ark]' && pip3 install requests

ENV PUB_SUB_EP=na
ENV PUB_SUB_TOPIC=na
ENV X_API_APPID=na
ENV X_API_TOKEN=na
ENV ARK_API_KEY=na
ENV ARK_API_ENGPOINT_ID=na

CMD ["python3", "main.py"]
