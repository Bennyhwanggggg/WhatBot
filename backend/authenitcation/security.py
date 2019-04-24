"""
    Helper functions for authentication
"""
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


def generate_token(user_type, user_id):
    """Generate a token using the SECRET_KEY from the configuration

    :param user_type: user's authority level, either student or admin
    :type: str
    :param user_id: user's username
    :type: str
    :return: token
    :rtype: str
    """
    s = Serializer(SECRET_KEY, expires_in=TOKEN_EXPIRE_TIME)
    token = s.dumps({'user_type': user_type, 'user_id': user_id})
    return token.decode()


def verify_token(token):
    """Check if a token is valid. It is not valid if expired or bad signature.

    :param token: authentication token
    :type: str
    :return: data if valid else None
    :rtype: str or None
    """
    s = Serializer(SECRET_KEY)
    try:
        data = s.loads(token)
    except (BadSignature, SignatureExpired):
        return None
    return data


def authenticate_admin_by_token(token):
    """Authenticate a token and check if user is admin

    :param token: authentication token
    :type: str
    :return: whether user is admin or not
    :rtype: bool
    """
    if token is None:
        return False
    if verify_token(token).user_type == 'admin':
        logger.debug('Authentication admin Success')
        return True
    logger.debug('Authentication admin fail')
    return False


def authenticate_student_by_token(token):
    """Authenticate a token and check if user is student

    :param token: authentication token
    :type: str
    :return: whether user is student or not
    :rtype: bool
    """
    if token is None:
        return False
    if verify_token(token).user_type == 'student':
        logger.debug('Authentication student Success')
        return True
    logger.debug('Authentication student fail')
    return False


def login_required_admin(f, message="You are not authorized"):
    """Decorator function to check if user is authorized as an admin to call an api
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("AUTH_TOKEN")
        if authenticate_admin_by_token(token):
            return f(*args, **kwargs)
        return jsonify(message=message), 401
    return decorated_function


def login_required(f, message="You are not authorized"):
    """Decorator function to check if user is authorized to call an api
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("AUTH_TOKEN")
        if authenticate_admin_by_token(token):
            return f(*args, **kwargs)
        if authenticate_student_by_token(token):
            return f(*args, **kwargs)
        return jsonify(message=message), 401
    return decorated_function
