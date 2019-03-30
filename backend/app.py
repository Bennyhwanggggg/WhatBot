from flask import Flask, request, abort, jsonify, flash
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime
import uuid
import os
from query_module.QueryModule import QueryModule
from response_module.ResponseModule import ResponseModule
from conf.Error import UploadFileError
from conf.Success import UploadFileSuccess

"""
    Initialize modules
"""
query_module = QueryModule()
response_module = ResponseModule()

"""
    Flask configuration setup
"""
app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = '/Users/mitsunari/Documents/UNSW/COMP9900-Info-Tech-Project/project/backend'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max size
ALLOWED_EXTENSIONS = set(['txt'])


@app.route('/login', methods=["post"])
def login():
    pass


@app.route('/upload', methods=["post"])
def upload():
    def allowed_file(f):
        return '.' in f and f.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    if 'file' not in request.files:
        return jsonify(message=UploadFileError.NO_FILE.value), 400
    file = request.files['file']
    if not file.filename:
        return jsonify(message=UploadFileError.NO_FILE_SELECTED.value)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename), 400
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # TODO: modify this to save in S3?
        return jsonify(message=UploadFileSuccess.SUCCESS.value), 200


@app.route('/message', methods=['POST'])
def message():
    # turning off authentication for now...
    # username = request.json.get('username', None)
    message = request.json.get('inputValue', None)
    id = str(uuid.uuid4())

    query_result = query_module.query(message)
    return_message = response_module.respond(query_result)
    response = {
        'message': return_message,
        'timestamp': datetime.now(),
        'id': id
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=9999)
