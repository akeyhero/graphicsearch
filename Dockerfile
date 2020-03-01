FROM tensorflow/tensorflow:1.15.0-py3 AS base

COPY requirements.txt /
RUN pip install -r requirements.txt

WORKDIR /app

# warming up; to download model parameters
COPY app/vectorizer.py /app/
RUN (echo 'from vectorizer import Vectorizer'; echo 'Vectorizer().prepare()') | python

COPY app /app

CMD ["uvicorn", "app:app", "--uds=/run/uvicorn/app.sock"]
