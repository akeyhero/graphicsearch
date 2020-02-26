FROM tensorflow/tensorflow:1.15.0-py3 AS base

WORKDIR /app

COPY app/requirements.txt /app/
RUN pip install -r requirements.txt

# warming up; to download model parameters
COPY app/vectorizer.py /app/
RUN (echo 'from vectorizer import Vectorizer'; echo 'Vectorizer().prepare()') | python


# --- development ---
FROM base as development

CMD ["uwsgi", "--ini=uwsgi.ini:development"]


# --- production ---
FROM base as production

COPY app /app

CMD ["uwsgi", "--ini=uwsgi.ini"]
