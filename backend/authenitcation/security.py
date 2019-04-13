from functools import wraps
from flask import request,jsonify
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from authenitcation.config import SECRET_KEY, TOKEN_EXPIRE_TIME
from conf.Logger import Logger

"""
    Logger setup
"""
logger = Logger(__name__).log


def generate_token(user_type):
    s = Serializer(SECRET_KEY, expires_in=TOKEN_EXPIRE_TIME)
    token = s.dumps(user_type)
    return token.decode()


def verify_token(token):
    s = Serializer(SECRET_KEY)
    try:
        data = s.loads(token)
    except (BadSignature, SignatureExpired):
        return None
    return data


def authenticate_admin_by_token(token):
    if token is None:
        return False
    if verify_token(token) == 'admin':
        logger.debug('Authentication admin Success')
        return True
    logger.debug('Authentication admin fail')
    return False


def authenticate_student_by_token(token):
    if token is None:
        return False
    if verify_token(token) == 'student':
        logger.debug('Authentication student Success')
        return True
    logger.debug('Authentication student fail')
    return False


def login_required_admin(f, message="You are not authorized"):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("AUTH_TOKEN")
        if authenticate_admin_by_token(token):
            return f(*args, **kwargs)
        return jsonify(message=message), 401
    return decorated_function


def login_required(f, message="You are not authorized"):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("AUTH_TOKEN")
        if authenticate_admin_by_token(token):
            return f(*args, **kwargs)
        if authenticate_student_by_token(token):
            return f(*args, **kwargs)
        return jsonify(message=message), 401
    return decorated_function
