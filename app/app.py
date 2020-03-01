#!/usr/bin/env python

import io
from typing import List, Dict
from threading import Lock

from fastapi import FastAPI, File
from pydantic import BaseModel
import tensorflow as tf

from vectorizer import Vectorizer
from elasticsearch_interface import ElasticsearchInterface


INDEX_NAME = 'image_net_b0'

app = FastAPI(
    title="Graphicsearch",
    description="An Elasticsearch based image search engine powered by deep learning",
    version="0.0.0",
)
lock = Lock()


class RootOut(BaseModel):
    message: str


class IndexOut(BaseModel):
    message: str
    es_response: Dict


class SearchOut(BaseModel):
    message: str
    es_response: Dict


@app.get('/', response_model=RootOut)
def root():
    return RootOut(message='OK')


@app.post('/index', response_model=IndexOut, status_code=201)
def index(file: bytes = File(...)):
    global elasticsearch_interface
    image_vector = vectorize(file)
    return IndexOut(message='OK', es_response=elasticsearch_interface.index_image(image_vector))

 
@app.post('/search', response_model=SearchOut)
def search(file: bytes = File(...)):
    global elasticsearch_interface
    image_vector = vectorize(file)
    return SearchOut(message='OK', es_response=elasticsearch_interface.search_image(image_vector))


def vectorize(image_bin):
    global lock, session, graph, vectorizer
    image_io = io.BytesIO(image_bin)
    with lock:
        with session.as_default():
            with graph.as_default():
                return vectorizer.vectorize(image_io)


def prepare():
    global session, graph, vectorizer, elasticsearch_interface
    session = tf.compat.v1.Session()
    graph = tf.compat.v1.get_default_graph()
    vectorizer = Vectorizer()
    with lock:
        with session.as_default():
            with graph.as_default():
                vectorizer.prepare()
    elasticsearch_interface = ElasticsearchInterface(INDEX_NAME)


prepare()
