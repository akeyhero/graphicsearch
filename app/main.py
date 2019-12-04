from flask import Flask, request, abort
app = Flask(__name__)

from vectorizer import Vectorizer

cache = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' in request.files:
            image_file = request.files['file']
            return str(vectorize(image_file)), 201
        else:
            return 'Unprocessible Entity', 422
    else:
        return 'OK', 200
 
@app.route('/search', methods=['POST'])
def search():
    if 'file' in request.files:
        image_file = request.files['file']
        return str(vectorize(image_file)), 200
    else:
        return 'Unprocessible Entity', 422

@app.before_first_request
def prepare():
    cache['vectorizer'] = Vectorizer().prepare()

def vectorize(image_file):
    return cache['vectorizer'].vectorize(image_file)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
