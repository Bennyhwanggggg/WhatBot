from flask import (Flask, request, abort, jsonify)

app = Flask(__name__)

users = []

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




if __name__ == '__main__':
    app.run(debug=True)