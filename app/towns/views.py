from flask import Blueprint, request, jsonify

from app.baseviews import required_args
from app.towns.models import Town
from app.app import session
from sqlalchemy import exc

towns = Blueprint('towns', __name__)


@towns.route('/api_v1.0/create_town', methods=['POST'])
@required_args(['name', 'id_country'])
def api_create_town():
    if 'name' in request.args:
        try:
            new_town = Town(name=request.args['name'], id_country=request.args['id_country'])
            session.add(new_town)
            session.commit()
        except exc.IntegrityError as e:
            session.rollback()
            return jsonify({'message': 'Duplicate value', 'data': None, 'status': 'error'}), 400
    return jsonify({'message': None, 'data': None, 'status': 'success'}), 201


@towns.route('/api_v1.0/get_towns', methods=['GET'])
def api_get_towns():
    d = {}
    q = session.query(Town)
    if 'id_country' in request.args:
        q.filter(Town.id_country == request.args['id_country'])
    for i, town in enumerate(q):
        d[i] = {'id_town': town.id_town,
                'name': town.name,
                'description': town.description,
                'url_photo': town.url_photo}
    return jsonify({'message': None, 'data': d, 'status': 'success'}), 200
