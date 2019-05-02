from functools import wraps

import jwt
from flask import request, jsonify

from app.app import session
from app.config import SECRET_KEY
from app.exceptions import InvalidUsage
from app.users.models import Users


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'token' in request.args:
            token = request.args['token']
        if not token:
            return jsonify({'message': 'Token is missing!', 'data': None, 'status': 'error'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY)
            current_user = session.query(Users).filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!', 'data': None, 'status': 'error'}), 401
        return f(current_user, *args, **kwargs)

    return decorated


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'token' in request.args:
            token = request.args['token']
        if not token:
            return jsonify({'message': 'Token is missing!', 'data': None, 'status': 'error'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY)
            current_user = session.query(Users).filter_by(public_id=data['public_id']).first()
            if current_user.id_role not in [1, 2]:
                raise Exception('Action is not required')
        except Exception as e:
            return jsonify({'message': e.args[0], 'data': None, 'status': 'error'}), 401
        return f(current_user, *args, **kwargs)

    return decorated


def required_args(_args):
    def decorator(func):
        @wraps(func)
        def newfn():
            errors = {}
            for a in _args:
                if a not in request.args:
                    errors[a] = 'This field is required'
            if errors:
                raise InvalidUsage(payload={'errors': errors})
            return func()
        return newfn
    return decorator