from flask import (Flask, request, abort, jsonify)
from datetime import datetime
import uuid

app = Flask(__name__)

users = []
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



@app.route('/send', methods = ["post"])
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




if __name__ == '__main__':
    app.run(debug=True)