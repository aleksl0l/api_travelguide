from flask import Blueprint, request, jsonify

from app.baseviews import required_args
from app.users.models import Users
from app.app import session
from app.config import SECRET_KEY
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime


users = Blueprint('users', __name__)


@users.route('/api_v1.0/create_user', methods=['GET', 'POST'])
@required_args(['name', 'password'])
def api_create_user():
    data = request.args.to_dict(flat=True)
    hashed_password = generate_password_hash(data['password'], method='sha256')
    try:
        new_user = Users(public_id=str(uuid.uuid4()),
                         name=data['name'],
                         password=hashed_password,)
        new_user.id_role = 3
        session.add(new_user)
        session.commit()
        return jsonify({'message': None, 'data': None, 'status': 'success'}), 201
    except Exception as e:
        session.rollback()
        return jsonify({'message': 'Unexpected error', 'data': None, 'status': 'error'}), 400


@users.route('/api_v1.0/get_user', methods=['GET'])
def api_get_user():
    d = {}
    q = session.query(Users)
    for i, user in enumerate(q):
        d[i] = {'public_id': user.public_id,
                'name': user.name,
                'id_role': user.id_role,}
    return jsonify({'message': None, 'data': d, 'status': 'success'}), 200


@users.route('/api_v1.0/login', methods=['GET', 'POST'])
@required_args(['name', 'password'])
def api_login_user():
    name = request.args['name']
    passw = request.args['password']
    user = session.query(Users).filter_by(name=name).first()
    if not user:
        return jsonify({'message': 'Password or user is invalid', 'data': None, 'status': 'error'}), 400

    if check_password_hash(user.password, passw):
        token = jwt.encode({'public_id': user.public_id,
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=10)},
                           SECRET_KEY)
        return jsonify({'message': None, 'data': {'token': token.decode('UTF-8')}, 'status': 'success'}), 200

    return jsonify({'message': 'Unexpected error', 'data': None, 'status': 'error'}), 400
