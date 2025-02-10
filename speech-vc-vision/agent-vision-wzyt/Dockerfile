FROM python:3.9-slim

WORKDIR /app

ADD main.py /app

RUN pip3 install 'confluent-kafka' && pip3 install --upgrade 'volcengine-python-sdk[ark]'

CMD ["python3", "main.py"]
