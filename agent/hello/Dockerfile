FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir Flask requests 

EXPOSE 8002

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=8002"]
