from flask import (Flask, request, abort, jsonify)
from datetime import datetime
import uuid

app = Flask(__name__)

users = []
# holds message ids in order
chat = []
messages = dict()

@app.route('/')
def my_index():
    #return flask.render_template("index.html", token="Hello Flask+React")
    return "hello"


@app.route('/login', methods = ["post"])
def login():
    #if you do not pass username, then the default will be None
    username = request.json.get('username', None)
    if username is None or username in users:
        abort(401)
    else:
        users.append(username)
        print(users)
        return jsonify({'status': 'OK', 'message': 'Successfully logged in'})



@app.route('/messages', methods = ["post"])
def send():
    username = request.json.get('username', None)
    message = request.json.get('message', None)

    if username is None or username not in users:
        abort(401)

    #'messsage is None' is allowed message to be empty, so need to check the empty
    if message is None or message == '':
        abort(401)

    id = str(uuid.uuid4())
    messages[id] = {
        'username': username,
        'message': message,
        'timestamp': datetime.now(),
        'id': id
    }

    chat.append(id)
    return jsonify(messages)


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
    app.run(debug=True, host='0.0.0.0')