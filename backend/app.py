from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime
import uuid
import json
import logging
import time
import os
import concurrent.futures

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
ALLOWED_EXTENSIONS = set(['txt'])  # We only allow .txt files to be uploaded
thread_executor = concurrent.futures.ThreadPoolExecutor(max_workers=16)

"""
    Path setup
"""
PATH = os.path.dirname(os.path.realpath(__file__))
INTENT_PATH = os.path.join(PATH, 'query_module/training_data/intents/')
ENTITY_PATH = os.path.join(PATH, 'query_module/training_data/entities/')
TEMP_PATH = os.path.join(PATH, 'management_module/temp/')


@app.route('/login', methods=['POST'])
def login():
    pass


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
    id = request.json.get('id', None)

    query_result = query_module.query(message)
    # use multiprocessing to avoid collecting user data from slowing us down
    thread_executor.submit(management_module.add_intent_data(query_result.intent, message, query_result.confidence))
    return_message = response_module.respond(query_result)

    response = {
        'message': return_message,
        'timestamp': datetime.now(),
        'id': id
    }
    return jsonify(response), 200


@app.route('/dashboard/piechart', methods=["GET"])
def piechart():
    # TODO original_data should come from database
    original_data = {
        "consultation_booking": 335,
        "prerequisites_queries": 310,
        "indicative_hours_queries": 234,
        "course_outline_queries": 1135,
        "course_location_queries": 1548,
    }

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


@app.route('/dashboard/timeline', methods=["GET"])
def timeline_chart():
    original_data = {
        "consultation_booking": [120, 132, 101, 134, 90, 230, 210],
        "prerequisites_queries": [220, 182, 191, 234, 290, 330, 310],
        "indicative_hours_queries": [150, 232, 201, 154, 190, 330, 410],
        "course_outline_queries": [320, 332, 301, 334, 390, 330, 320],
        "course_location_queries": [820, 932, 901, 934, 1290, 1330, 1320]
    }
    time_slots = [
        "07/04/2019",
        "08/04/2019",
        "09/04/2019",
        "10/04/2019",
        "11/04/2019",
        "12/04/2019",
        "13/04/2019",
    ]

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


@app.route('/dashboard/barchart', methods=["GET"])
def barchart():
    category_data = ["consultation_booking",
                     "prerequisites_queries",
                     "indicative_hours_queries",
                     "course_outline_queries",
                     "course_location_queries_followup",
                     "indicative_hours_queries_followup",
                     "prerequisites_queries_followup",]
    confidence_data = [0.78, 0.82, 0.85, 0.87, 0.89, 0.90, 0.91]
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
JSON_3D_PATH = os.path.join("3d-table.json")


@app.route('/dashboard/3dchart', methods=["GET"])
def three_dimention_chart():
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
                'Income',
                'Time',
                'Population',
                'Intent',
                {"name": 'Year', "type": 'ordinal'}
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


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=9999)
