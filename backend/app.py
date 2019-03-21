from flask import (Flask, request, abort, jsonify)
from flask_cors import CORS
from datetime import datetime
import uuid
from query_module.QueryModule import QueryModule
from response_module.ResponseModule import ResponseModule
from conf.Response import IntentResponse, FallbackResponse

query_module = QueryModule()
response_module = ResponseModule()

app = Flask(__name__)
CORS(app)


@app.route('/login', methods=["post"])
def login():
    pass


@app.route('/message', methods=["post"])
def message():
    # turning off authentication for now...
    # username = request.json.get('username', None)
    message = request.json.get('inputValue', None)
    id = str(uuid.uuid4())

    query_result = query_module.detect_intent_texts(message)
    return_message = response_module.respond(query_result)
    response = {
        'message': return_message,
        'timestamp': datetime.now(),
        'id': id
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=9999)
