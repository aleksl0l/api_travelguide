from flask import Blueprint, request, jsonify
from sqlalchemy import exc

from app.app import session
from app.baseviews import required_args
from app.sights.models import Sights

sights = Blueprint('sights', __name__)


@sights.route('/api_v1.0/create_sight', methods=['POST'])
def api_create_sights():
    try:
        args = request.args.to_dict(flat=True)
        try:
            args['urls'] = args['urls'].split(',')
        except KeyError as e:
            print(e)
        new_sight = Sights(**args)
        session.add(new_sight)
        session.commit()
    except exc.IntegrityError as e:
        session.rollback()
        return jsonify({'message': 'Duplicate value' + e.args[0], 'data': None, 'status': 'error'}), 400
    return jsonify({'message': None, 'data': None, 'status': 'success'}), 200


@sights.route('/api_v1.0/get_sights', methods=['GET'])
@required_args(['id_town'])
def api_get_sights():
    query = session.query(Sights)
    query = query.filter(Sights.id_town == request.args['id_town']).all()
    response_data = [sight.serialize() for sight in query]
    return jsonify({'message': None, 'data': response_data, 'status': 'success'}), 200


@sights.route('/api_v1.0/modify_sight', methods=['PUT'])
@required_args(['id_sight'])
def api_modify_sight():
    request_data = request.args.to_dict(flat=True)
    if 'tag' in request_data:
        request_data['tag'] = request_data['tag'].split(',')
    request_data.pop('id_sight')
    session.query(Sights).filter(Sights.id_sight == request.args['id_sight']).update(request_data)
    session.commit()
    return jsonify({'message': None, 'data': request_data, 'status': 'success'}), 200


@sights.route('/api_v1.0/add_img_to_sight', methods=['POST'])
@required_args(['id_sight', 'imgs'])
def api_add_img_to_sight():
    imgs = request.args['imgs'].split(',')
    query = session.query(Sights).filter(Sights.id_sight == request.args['id_sight']).first()
    query.urls = f'{query.urls}{imgs}' if query.urls else imgs
    session.commit()
    return jsonify({'message': None, 'data': None, 'status': 'success'}), 201
