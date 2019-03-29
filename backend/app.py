from flask import (Flask, request, abort, jsonify)
from flask_cors import CORS
from datetime import datetime
import uuid
from query_module.QueryModule import QueryModule
from response_module.ResponseModule import ResponseModule
from conf.Response import IntentResponse, FallbackResponse
import os

query_module = QueryModule()
response_module = ResponseModule()

app = Flask(__name__)
CORS(app)


@app.route('/login', methods=["post"])
def login():
    pass

@app.route('/', methods=["post"])
def test():
    return jsonify({'test': 'success'}), 200


@app.route('/message', methods=["post"])
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
    # if os.environ['BACKEND_NAME']:
    #     app.run(debug=True, host=os.environ['BACKEND_NAME'], port=9999)
    # else:
    app.run(debug=True, host='localhost', port=9999)
