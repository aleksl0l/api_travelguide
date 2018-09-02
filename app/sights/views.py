from flask import Blueprint, request, jsonify
from sqlalchemy import exc

from app.app import session
from app.baseviews import required_args
from app.sights.models import Sights

sights = Blueprint('sights', __name__)


@sights.route('/api_v1.0/create_sight', methods=['POST'])
@required_args(['id_town', 'name'])
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


@sights.route('/api_v1.0/get_sights', methods=['GET'])
@required_args(['id_town'])
def api_get_sights():
    d = []
    q = session.query(Sights)
    q = q.filter(Sights.id_town == request.args['id_town']).all()
    for i, sight in enumerate(q):
        d.append({'id_town': sight.id_town,
                  'id_sight': sight.id_sight,
                  'name': sight.name,
                  'tags': sight.tag,
                  'cost': sight.cost,
                  'coordinate': [sight.cord_lat, sight.cord_long],
                  'rating': sight.rating,
                  'type': sight.type_sight,
                  'photo_urls': sight.urls,
                  'web_site': sight.web_site,
                  'description': sight.description,
                  'history': sight.history,
                  'phone_number': sight.phone_number})
    return jsonify({'message': None, 'data': d, 'status': 'success'}), 200


@sights.route('/api_v1.0/modify_sight', methods=['PUT'])
@required_args(['id_sight'])
def api_modify_sight():
    d = request.args.to_dict(flat=True)
    if 'tag' in d:
        d['tag'] = d['tag'].split(',')
    d.pop('id_sight')
    session.query(Sights).filter(Sights.id_sight == request.args['id_sight']).update(d)
    session.commit()
    return jsonify({'message': None, 'data': d, 'status': 'success'}), 200


@sights.route('/api_v1.0/add_img_to_sight', methods=['POST'])
@required_args(['id_sight', 'imgs'])
def api_add_img_to_sight():
    imgs = request.args['imgs'].split(',')
    q = session.query(Sights).filter(Sights.id_sight == request.args['id_sight']).first()
    q.urls = q.urls + imgs if q.urls else imgs
    session.commit()
    return jsonify({'message': None, 'data': None, 'status': 'success'}), 201
