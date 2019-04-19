from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime
import json
import logging
import time
import os
import concurrent.futures

from query_module.QueryModule import QueryModule
from database.DataBaseManager import DataBaseManager
from response_module.ResponseModule import ResponseModule
from management_module.ManagementModule import ManagementModule
from conf.Error import UploadFileError, AuthenticationError
from conf.Success import UploadFileSuccess
from conf.Logger import Logger
from authenitcation.security import generate_token, verify_token
from authenitcation.db import Authenticator

"""
    Initialize modules
"""
database_manager = DataBaseManager()
query_module = QueryModule()
response_module = ResponseModule(database_manager=database_manager)
management_module = ManagementModule(database_manager=database_manager)
authenticator = Authenticator(database_manager=database_manager)

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
authentication_db_logger = logging.getLogger('authentication.db')
authentication_db_logger.setLevel(logging.DEBUG)
authentication_security_logger = logging.getLogger('authentication.security')
authentication_security_logger.setLevel(logging.DEBUG)

"""
    Flask configuration setup
"""
app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max size
ALLOWED_EXTENSIONS = set(['txt'])  # We only allow .txt files to be uploaded
thread_executor = concurrent.futures.ThreadPoolExecutor(max_workers=16)


@app.after_request
def after_request(resp):
    resp.headers["Access-Control-Allow-Origin"] = '*'
    request_headers = request.headers.get("Access-Control-Request-Headers")
    resp.headers["Access-Control-Allow-Headers"] = request_headers
    resp.headers['Access-Control-Allow-Methods'] = "DELETE, GET, POST, HEAD, OPTIONS"
    return resp


"""
    Path setup
"""
PATH = os.path.dirname(os.path.realpath(__file__))
INTENT_PATH = os.path.join(PATH, 'query_module/training_data/intents/')
ENTITY_PATH = os.path.join(PATH, 'query_module/training_data/entities/')
TEMP_PATH = os.path.join(PATH, 'management_module/temp/')


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username or not password:
        return jsonify(message=AuthenticationError.INVALID_CREDENTIALS.value), 401
    if authenticator.check_is_admin(username, password):
        return jsonify(token=generate_token('admin', username), id=username, authority='admin'), 200
    if authenticator.check_is_student(username, password):
        return jsonify(token=generate_token('student', username), id=username, authority='student'), 200
    logger.info('{}: {} login success'.format(username, password))
    return jsonify(message=AuthenticationError.INVALID_CREDENTIALS.value), 401


@app.route('/validation', methods=['POST'])
def validation():
    token = request.headers.get('authorization', None)
    if not token:
        return jsonify(message=AuthenticationError.INVALID_CREDENTIALS.value), 401
    verified = verify_token(token)
    if not verified:
        return jsonify(message=AuthenticationError.INVALID_CREDENTIALS.value), 401
    logger.info('{}: {} re-authenticated'.format(verified['user_id'], verified['user_type']))
    return jsonify(token=token, id=verified['user_id'], authority=verified['user_type']), 200


@app.route('/upload', methods=['POST'])
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
    username = request.json.get('username', None)
    id = request.json.get('id', None)

    query_result = query_module.query(message)
    # use multiprocessing to avoid collecting user data from slowing us down
    thread_executor.submit(management_module.add_intent_data(query_result.intent, message, query_result.confidence))
    query_result.set_username(username)
    return_message = response_module.respond(query_result)

    response = {
        'message': return_message.strip(),
        'timestamp': datetime.now(),
        'id': id
    }
    return jsonify(response), 200


@app.route('/dashboard/piechart', methods=['GET'])
def piechart():
    data = management_module.get_intent_percentages(n=8)
    original_data = dict()
    for intent, value in data:
        original_data[intent] = value

    # convert the original data to the form that echart piechart expected
    key_list = list(original_data.keys())
    data_field = [{"value": original_data[key], "name": key} for key in key_list]
    response_data = {
        "tooltip": {
            "trigger": "item",
            "formatter": "{a} <br/>{b}: {c} ({d}%)"
        },
        "legend": {
            "orient": "vertical",
            "x": "left",
            "data": key_list
        },
        "series": [
            {
                "name": "intents",
                "type": "pie",
                "radius": ["50%", "70%"],
                "avoidLabelOverlap": False,
                "label": {
                    "normal": {
                        "show": False,
                        "position": "center"
                    },
                    "emphasis": {
                        "show": True,
                        "textStyle": {
                            "fontSize": "30",
                            "fontWeight": "bold"
                        }
                    }
                },
                "labelLine": {
                    "normal": {
                        "show": False
                    }
                },
                "data": data_field
            }
        ]
    }

    response_data = {
        "data": response_data
    }
    return jsonify(response_data), 200


@app.route('/dashboard/timeline', methods=['GET'])
def timeline_chart():
    original_data, time_slots = management_module.get_intent_timeline()
    title_list = list(original_data.keys())
    series_list = [
        {
            "name": title,
            "type": 'line',
            "stack": i,
            "data": original_data[title],
        }
        for i, title in enumerate(original_data)
    ]
    response_data = {
        "title": {
            "text": ' '
        },
        "tooltip": {
            "trigger": 'axis'
        },
        "legend": {
            "data": title_list
        },
        "grid": {
            "left": '3%',
            "right": '4%',
            "bottom": '3%',
            "containLabel": True
        },
        "toolbox": {
            "feature": {
                "saveAsImage": {}
            }
        },
        "xAxis": {
            "type": 'category',
            "boundaryGap": False,
            "data": time_slots
        },
        "yAxis": {
            "type": 'value'
        },

        "series": series_list
    }
    response_data = {
        "data": response_data
    }
    return jsonify(response_data), 200


@app.route('/dashboard/barchart', methods=['GET'])
def barchart():
    original_data = management_module.get_avg_confidence()
    category_data = [item[0] for item in original_data]
    confidence_data = [round(item[1], 2) for item in original_data]
    response_data = {
        "color": ['#3398DB'],
        "tooltip": {
            "trigger": 'axis',
            "axisPointer": {
                "type": 'shadow'
            }
        },
        "grid": {
            "left": '3%',
            "right": '4%',
            "bottom": '3%',
            "containLabel": True
        },
        "xAxis": [
            {
                "type": 'category',
                "data": category_data,
                "axisTick": {
                    "alignWithLabel": True
                }
            }
        ],
        "yAxis": [
            {
                "type": 'value'
            }
        ],
        "series": [
            {
                "name": 'Average Confidence',
                "type": 'bar',
                "barWidth": '60%',
                "data": confidence_data
            }
        ]
    }
    response_data = {
        "data": response_data
    }
    return jsonify(response_data), 200


PATH = os.path.dirname(os.path.realpath(__file__))
JSON_3D_PATH = os.path.join("filter3.json")


@app.route('/dashboard/3dchart', methods=['GET'])
def three_dimention_chart():
    # TODO: create a function for this
    with open(JSON_3D_PATH) as f:
        data = json.load(f)
    symbol_size = 2.5
    response_data = {
        "grid3D": {},
        "xAxis3D": {
            "type": 'category'
        },
        "yAxis3D": {},
        "zAxis3D": {},
        "dataset": {
            "dimensions": [
                'Usage',
                'Time',
                'Intent',
                {"name": 'Intent', "type": 'ordinal'}
            ],
            "source": data
        },
        "series": [
            {
                "type": 'scatter3D',
                "symbolSize": symbol_size,
                "encode": {
                    "x": 'Intent',
                    "y": 'Time',
                    "z": 'Usage',
                    "tooltip": [0, 1, 2, 3, 4]
                }
            }
        ]
    }
    response_data = {
        "data": response_data
    }
    return jsonify(response_data), 200


@app.route('/', methods=['GET'])
def setup():
    logger.info('backend activated')
    return jsonify(message='success'), 200


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=9999)
