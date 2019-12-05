FROM tensorflow/tensorflow:1.15.0-py3 AS graphicsearch

WORKDIR /app

COPY app/requirements.txt /app/
RUN pip install -r requirements.txt

# warming up
COPY app/vectorizer.py /app/
RUN (echo 'from vectorizer import Vectorizer'; echo 'Vectorizer().prepare()') | python

COPY app /app

CMD ["python", "main.py"]
