#!/usr/bin/env python

from flask import Flask, request, abort
app = Flask(__name__)

import tensorflow as tf
from vectorizer import Vectorizer
from elasticsearch_interface import ElasticsearchInterface

INDEX_NAME = 'image_net_b0'

@app.route('/', methods=['GET', 'POST'])
def index():
    global elasticsearch_interface
    if request.method == 'POST':
        if 'file' in request.files:
            image_file = request.files['file']
            image_vector = vectorize(image_file)
            return elasticsearch_interface.index_image(image_vector), 201
        else:
            return 'Unprocessible Entity', 422
    else:
        return 'OK', 200
 
@app.route('/search', methods=['POST'])
def search():
    global elasticsearch_interface
    if 'file' in request.files:
        image_file = request.files['file']
        image_vector = vectorize(image_file)
        return elasticsearch_interface.search_image(image_vector), 200
    else:
        return 'Unprocessible Entity', 422

def vectorize(image_file):
    global session, graph, vectorizer
    with session.as_default():
        with graph.as_default():
            return vectorizer.vectorize(image_file)

def prepare():
    global session, graph, vectorizer, elasticsearch_interface
    session = tf.compat.v1.Session()
    graph = tf.compat.v1.get_default_graph()
    vectorizer = Vectorizer()
    with session.as_default():
        with graph.as_default():
            vectorizer.prepare()
    elasticsearch_interface = ElasticsearchInterface(INDEX_NAME)

if __name__ == "__main__":
    prepare()
    app.run(host='0.0.0.0')
