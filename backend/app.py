from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer)
import uuid
import logging
import time
import os

from query_module.QueryModule import QueryModule
from response_module.ResponseModule import ResponseModule
from management_module.ManagementModule import ManagementModule
from conf.Error import UploadFileError
from conf.Success import UploadFileSuccess
from conf.Logger import Logger
from authenitcation.config import SECRET_KEY
from authenitcation.security import login_required

"""
    Initialize modules
"""
query_module = QueryModule()
response_module = ResponseModule()
management_module = ManagementModule()

"""
    Logger configurations. By default all are set to DEBUG level.
    Change the level in setLevel to suit whatever your needs are.
    Available levels from highest severity to lowest are:
        CRITICAL
        ERROR
        WARNING
        INFO
        DEBUG
"""
logger = Logger(__name__).log
logger.setLevel(logging.INFO)
query_module_logger = logging.getLogger('query_module.QueryModule')
query_module_logger.setLevel(logging.INFO)
train_logger = logging.getLogger('query_module.train')
train_logger.setLevel(logging.INFO)
response_module_logger = logging.getLogger('response_module.ResponseModule')
response_module_logger.setLevel(logging.INFO)
database_logger = logging.getLogger('database.DataBaseManager')
database_logger.setLevel(logging.INFO)
management_logger = logging.getLogger('management_module.ManagementModule')
management_logger.setLevel(logging.INFO)

"""
    Flask configuration setup
"""
app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max size
ALLOWED_EXTENSIONS = set(['txt'])  # We only allow .txt files to be uploaded

"""
    Path setup
"""
PATH = os.path.dirname(os.path.realpath(__file__))
INTENT_PATH = os.path.join(PATH, 'query_module/training_data/intents/')
ENTITY_PATH = os.path.join(PATH, 'query_module/training_data/entities/')
TEMP_PATH = os.path.join(PATH, 'management_module/temp/')


@app.route('/login', methods=["post"])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username or not password:
        return 404
    s = Serializer(SECRET_KEY, expires_in=6000)
    token = s.dumps(username)
    if username == 'admin' and password == 'admin':  # TODO: search through database and if there is a match, use its type to identify user and use that to generate token
        return token.decode()
    return 404


@app.route('/upload', methods=["post"])
def upload():
    def allowed_file(f):
        return '.' in f and f.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    if 'file' not in request.files:
        return jsonify(message=UploadFileError.NO_FILE.value), 400
    file = request.files['file']
    if not file.filename:
        return jsonify(message=UploadFileError.NO_FILE_SELECTED.value), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(TEMP_PATH, "{}-{}.txt".format(filename.rstrip('.txt'), int(time.time())))
        file.save(file_path)
        if not management_module.train(file_path):
            os.remove(file_path)
            return jsonify(message=UploadFileError.INVALID_FORMAT.value), 400
        return jsonify(message=UploadFileSuccess.SUCCESS.value), 200


@app.route('/message', methods=['POST'])
def message():
    message = request.json.get('inputValue', None)
    id = request.json.get('id', None)

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
