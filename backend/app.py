from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime
import uuid
import logging

from query_module.QueryModule import QueryModule
from response_module.ResponseModule import ResponseModule
from management_module.ManagementModule import ManagementModule
from conf.Error import UploadFileError
from conf.Success import UploadFileSuccess
from conf.Logger import Logger

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
        management_module.upload_new_file(filename)
        # TODO: automated training
        return jsonify(message=UploadFileSuccess.SUCCESS.value), 200


@app.route('/message', methods=['POST'])
def message():
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
