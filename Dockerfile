FROM tensorflow/tensorflow:1.15.0-py3 AS graphicsearch

RUN pip install efficientnet==1.0.* keras==2.3.* Flask==1.1.*

WORKDIR /app

COPY app/vectorizer.py /app/

# warming up
RUN (echo 'from vectorizer import Vectorizer'; echo 'Vectorizer().prepare()') | python

COPY app /app

CMD ["python", "main.py"]
