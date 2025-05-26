FROM python:3.9-slim

WORKDIR /app

ADD restapp.py /app

EXPOSE 5000

RUN pip3 install 'flask' && pip3 install 'tos' && pip3 install 'markdown' && pip3 install 'python-docx'  && pip3 install 'gunicorn'   

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "restapp:app"]
