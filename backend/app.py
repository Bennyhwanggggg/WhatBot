from flask import (Flask, request, abort, jsonify)
from flask_cors import CORS
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)

users = []
# holds message ids in order
chat = []
messages = dict()


@app.route('/login', methods=["post"])
def login():
    #if you do not pass username, then the default will be None
    username = request.json.get('username', None)
    if username is None or username not in users:
        abort(401)
    else:
        users.append(username)
        print(users)
        return jsonify({'status': 'OK', 'message': 'Successfully logged in'})


@app.route('/message', methods=["post"])
def message():
    # turning off authentication for now...
    # username = request.json.get('username', None)
    message = request.json.get('inputValue', None)
    id = str(uuid.uuid4()) if request.json.get('id', None) is None else str(uuid.uuid4())

    response = {
        # 'username': username,
        'message': 'This is the response to {}'.format(message),
        'timestamp': datetime.now(),
        'id': id
    }

    chat.append(id)
    return jsonify(response)


@app.route('/get/<last_id>', methods = ["GET"])
def get(last_id):
    if chat is None or len(chat) == 0:
        return []
    index = get_next_index(last_id) if last_id else 0
    print(index)

    ids_to_return = chat[index:]
    print(ids_to_return)
    results = map(lambda x: messages[x], ids_to_return)
    print(results)
    return jsonify(list(results))


@app.route('/updates/<last_id>', methods = ["GET"])
def updates(last_id):
    index = get_next_index(last_id) if last_id else 0

    result = {
        'new_messages': False
    }

    if index < len(chat):
        result['new_messages'] = True
    return jsonify(result)


def get_next_index(last_id):
    try:
        return chat.index(last_id) + 1
    except ValueError as e:
        abort(400)


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=9999)
