from main import app, session
from flask import request, jsonify
from model import Country, Town, Sights, Users, Roles, Likes
from sqlalchemy import exc
import jwt
import datetime
from functools import wraps
import uuid
from werkzeug.security import generate_password_hash, check_password_hash


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'token' in request.args:
            token = request.args['token']
        if not token:
            return jsonify({'message': 'Token is missing!', 'data': None, 'status': 'error'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
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
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = session.query(Users).filter_by(public_id=data['public_id']).first()
            if current_user.id_role not in [1, 2]:
                raise Exception('Action is not required')
        except Exception as e:
            return jsonify({'message': e.args[0], 'data': None, 'status': 'error'}), 401
        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/api_v1.0', methods=['GET', 'POST'])
def api_root():
    return ')'


@app.route('/api_v1.0/create_country', methods=['GET', 'POST'])
def api_create_country():
    print(request.args)
    if 'name' in request.args:
        new_count = Country(name=request.args['name'])
        try:
            session.add(new_count)
            session.commit()
        except exc.IntegrityError:
            session.rollback()
            return jsonify({'message': 'Duplicate value', 'data': None, 'status': 'error'})
    return jsonify({'message': None, 'data': None, 'status': 'success'})


@app.route('/api_v1.0/get_countries', methods=['GET', 'POST'])
def api_get_countries():
    d = {}
    q = session.query(Country)
    if 'id_country' in request.args:
        q = q.filter(Country.id_country == request.args['id_country'])
    for i, country in enumerate(q):
        d[i] = {'id_town': country.id_country, 'name': country.name}
    return jsonify({'message': None, 'data': d, 'status': 'success'})


@app.route('/api_v1.0/create_town', methods=['GET', 'POST'])
def api_create_town():
    print(request.args)
    if 'name' in request.args:
        try:
            new_town = Town(name=request.args['name'], id_country=2)
            session.add(new_town)
            session.commit()
        except exc.IntegrityError:
            session.rollback()
            return jsonify({'message': 'Duplicate value', 'data': None, 'status': 'error'})
    return jsonify({'message': None, 'data': None, 'status': 'success'})


@app.route('/api_v1.0/get_towns', methods=['GET', 'POST'])
def api_get_towns():
    d = {}
    q = session.query(Town)
    if 'id_country' in request.args:
        q.filter(Town.id_country == request.args['id_country'])
    for i, town in enumerate(q):
        d[i] = {'id_town': town.id_town, 'name': town.name, 'description': town.description}
    return jsonify({'message': None, 'data': d, 'status': 'success'})


@app.route('/api_v1.0/create_sight', methods=['GET', 'POST'])
def api_create_sights():
    print(request.args.to_dict(flat=True))
    if 'id_town' in request.args and 'name' in request.args:
        try:
            args = request.args.to_dict(flat=True)
            try:
                args['urls'] = args['urls'].split(',')
                print(args['urls'])
            except KeyError as e:
                print(e)
            new_sight = Sights(**args)
            session.add(new_sight)
            session.commit()
        except exc.IntegrityError as e:
            session.rollback()
            return jsonify({'message': 'Duplicate value' + e.args[0], 'data': None, 'status': 'error'})
    return jsonify({'message': None, 'data': None, 'status': 'success'})


@app.route('/api_v1.0/get_sights', methods=['GET', 'POST'])
def api_get_sights():
    d = {}
    q = session.query(Sights)
    if 'id_town' in request.args:
        q = q.filter(Sights.id_town == request.args['id_town'])
        for i, sight in enumerate(q):
            d[i] = {'id_town': sight.id_town,
                    'id_sight': sight.id_sights,
                    'name': sight.name,
                    'tags': sight.tag,
                    'cost': sight.cost,
                    'coordinate': sight.coordinate,
                    'rating': sight.rating,
                    'type': sight.type_sight,
                    'photo_urls': sight.urls
                    }
        return jsonify({'message': None, 'data': d, 'status': 'success'})
    else:
        return jsonify({'message': 'Field id_town is required', 'data': None, 'status': 'error'})


@app.route('/api_v1.0/modify_sight', methods=['GET', 'POST'])
def api_modify_sight():
    if 'id_sight' in request.args:
        d = request.args.to_dict(flat=True)
        if 'tag' in d:
            d['tag'] = d['tag'].split(',')
        d.pop('id_sight')
        print(type(d), d)
        session.query(Sights).filter(Sights.id_sights == request.args['id_sight']).update(d)
        session.commit()
        return jsonify({'message': None, 'data': d, 'status': 'success'})
    else:
        return jsonify({'message': 'Field id_sight is required', 'data': None, 'status': 'error'})


@app.route('/api_v1.0/create_user', methods=['GET', 'POST'])
def api_create_user():
    data = request.args.to_dict(flat=True)
    hashed_password = generate_password_hash(data['password'], method='sha256')
    try:
        new_user = Users(public_id=str(uuid.uuid4()),
                         name=data['name'],
                         password=hashed_password,
                         id_role=3)
        session.add(new_user)
        session.commit()
        return jsonify({'message': None, 'data': None, 'status': 'success'})
    except Exception as e:
        session.rollback()
        return jsonify({'message': 'Unexpected error', 'data': None, 'status': 'error'})


@app.route('/api_v1.0/get_user', methods=['GET', 'POST'])
def api_get_user():
    d = {}
    q = session.query(Users)
    try:
        for i, user in enumerate(q):
            d[i] = {'public_id': user.public_id,
                    'name': user.name,
                    'id_role': user.id_role,
                    }
        return jsonify({'message': None, 'data': d, 'status': 'success'})
    except Exception as e:
        return jsonify({'message': e.args, 'data': d, 'status': 'success'})


@app.route('/api_v1.0/login', methods=['GET', 'POST'])
def api_login_user():
    name = request.args['name']
    passw = request.args['password']
    user = session.query(Users).filter_by(name=name).first()
    print(name, passw)
    if not user:
        return jsonify({'message': 'Password or user is invalid', 'data': None, 'status': 'error'})

    if check_password_hash(user.password, passw):
        token = jwt.encode({'public_id': user.public_id,
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=10)},
                           app.config['SECRET_KEY'])
        return jsonify({'message': None, 'data': {'token': token.decode('UTF-8')}, 'status': 'success'})

    return jsonify({'message': 'Unexpected error', 'data': None, 'status': 'error'})


@app.route('/api_v1.0/add_like', methods=['GET', 'POST'])
@token_required
def api_add_like(current_user):
    try:
        id_sight = request.args['id_sight']
        new_like = Likes(id_user=current_user.id_user, id_sight=id_sight, value=1)
        session.add(new_like)
        session.commit()
        return jsonify({'message': None, 'data': None, 'status': 'success'})
    except exc.IntegrityError:
        session.rollback()
        return jsonify({'message': 'Duplicate', 'data': None, 'status': 'error'})
    except Exception as e:
        session.rollback()
        return jsonify({'message': 'Unexpected error', 'data': None, 'status': 'error'})


@app.route('/api_v1.0/del_like', methods=['GET', 'POST'])
@token_required
def api_del_like(current_user):
    try:
        id_sight = request.args['id_sight']
        del_like = session.query(Likes).filter(
                                               Likes.id_user == current_user.id_user,
                                               Likes.id_sight == id_sight
                                            ).first()
        session.delete(del_like)
        session.commit()
        return jsonify({'message': None, 'data': None, 'status': 'success'})
    except Exception as e:
        session.rollback()
        return jsonify({'message': 'Unexpected error', 'data': None, 'status': 'error'})




