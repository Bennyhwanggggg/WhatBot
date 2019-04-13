from functools import wraps
from flask import request,jsonify
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer)
from authenitcation.config import SECRET_KEY


def authenticate_by_token(token):
    if token is None:
        return False
    s = Serializer(SECRET_KEY)
    username = s.loads(token.encode())
    if username == 'admin':
        return True
    return False


def login_required(f, message="You are not authorized"):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("AUTH_TOKEN")
        if authenticate_by_token(token):
            return f(*args, **kwargs)
        return jsonify(message=message), 401
    return decorated_function