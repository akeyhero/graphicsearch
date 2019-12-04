FROM tensorflow/tensorflow:1.15.0-py3 AS graphicsearch

RUN pip install efficientnet==1.0.* keras==2.3.* Flask==1.1.*

COPY app /app
WORKDIR /app

CMD ["python", "main.py"]
