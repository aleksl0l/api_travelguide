from flask import Blueprint, request, jsonify
from sqlalchemy import exc

from app.app import session
from app.sights.models import Sights

sights = Blueprint('sights', __name__)


@sights.route('/api_v1.0/create_sight', methods=['POST'])
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
            return jsonify({'message': 'Duplicate value' + e.args[0], 'data': None, 'status': 'error'}), 400
    return jsonify({'message': None, 'data': None, 'status': 'success'}), 201


@sights.route('/api_v1.0/get_sights', methods=['GET'])
def api_get_sights():
    d = []
    q = session.query(Sights)
    if 'id_town' in request.args:
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
                      'phone_number': sight.phone_number
                      })
        return jsonify({'message': None, 'data': d, 'status': 'success'}), 200
    else:
        return jsonify({'message': 'Field id_town is required', 'data': None, 'status': 'error'}), 400


@sights.route('/api_v1.0/modify_sight', methods=['PUT'])
def api_modify_sight():
    if 'id_sight' in request.args:
        d = request.args.to_dict(flat=True)
        if 'tag' in d:
            d['tag'] = d['tag'].split(',')
        d.pop('id_sight')
        print(type(d), d)
        session.query(Sights).filter(Sights.id_sights == request.args['id_sight']).update(d)
        session.commit()
        return jsonify({'message': None, 'data': d, 'status': 'success'}), 200
    else:
        return jsonify({'message': 'Field id_sight is required', 'data': None, 'status': 'error'}), 400


@sights.route('/api_v1.0/add_img_to_sight', methods=['POST'])
def api_add_img_to_sight():
    if 'id_sight' in request.args:
        imgs = request.args['imgs'].split(',')
        q = session.query(Sights).filter(Sights.id_sights == request.args['id_sight']).first()
        imgs += q.urls
        session.query(Sights).filter(Sights.id_sights == request.args['id_sight']).update({'urls': imgs})
        session.commit()
        return jsonify({'message': None, 'data': None, 'status': 'success'}), 201
    else:
        return jsonify({'message': 'Field id_sight is required', 'data': None, 'status': 'error'}), 400
