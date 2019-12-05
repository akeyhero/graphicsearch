from flask import Flask, request, abort
app = Flask(__name__)

from vectorizer import Vectorizer
from elasticsearch_interface import ElasticsearchInterface

INDEX_NAME = 'image_net_b0'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' in request.files:
            image_file = request.files['file']
            image_vector = vectorize(image_file)
            es = ElasticsearchInterface(INDEX_NAME)
            return es.index_image(image_vector), 201
        else:
            return 'Unprocessible Entity', 422
    else:
        return 'OK', 200
 
@app.route('/search', methods=['POST'])
def search():
    if 'file' in request.files:
        image_file = request.files['file']
        image_vector = vectorize(image_file)
        es = ElasticsearchInterface(INDEX_NAME)
        return es.search_image(image_vector), 200
    else:
        return 'Unprocessible Entity', 422

@app.before_first_request
def prepare():
    es = ElasticsearchInterface(INDEX_NAME)
    es.create_index()

def vectorize(image_file):
    # FIXME: This should be cached because this is too slow
    vectorizer = Vectorizer().prepare()
    return vectorizer.vectorize(image_file)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
