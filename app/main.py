from flask import Flask, request, abort
app = Flask(__name__)
 
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' in request.files:
            img_file = request.files['file']
            return 'Created', 201
        else:
            return 'Unprocessible Entity', 422
    else:
        return 'OK', 200
 
@app.route('/search', methods=['POST'])
def search():
    if 'file' in request.files:
        img_file = request.files['file']
    else:
        return 'Unprocessible Entity', 422

if __name__ == "__main__":
    app.run(host='0.0.0.0')
