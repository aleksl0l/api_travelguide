from flask import request, jsonify
from app.users.models import Users
import jwt
from functools import wraps
from app.app import session
from app.config import SECRET_KEY


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