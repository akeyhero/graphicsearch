FROM tensorflow/tensorflow:1.15.0-py3 AS base

WORKDIR /app

COPY app/requirements.txt /app/
RUN pip install -r requirements.txt

# warming up; to download model parameters
COPY app/vectorizer.py /app/
RUN (echo 'from vectorizer import Vectorizer'; echo 'Vectorizer().prepare()') | python


# --- development ---
FROM base as development

# FIXME: `--reload` could not be used due to `ModuleNotFoundError: No module named 'tensorflow_core.keras'`
CMD ["flask", "run", "--debugger", "--host=0.0.0.0"]


# --- production ---
FROM base as production

COPY app /app

# FIXME: This is not good for production environment
CMD ["./app.py"]
