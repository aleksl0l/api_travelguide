from flask import Blueprint, request, jsonify
from sqlalchemy import exc

from app.app import session
from app.baseviews import required_args
from app.towns.models import Town
from app.towns.utils import map_town

towns = Blueprint('towns', __name__)


@towns.route('/api_v1.0/create_town', methods=['POST'])
@required_args(['name', 'id_country'])
def api_create_town():
    if 'name' in request.args:
        try:
            new_town = Town(name=request.args['name'], id_country=request.args['id_country'])
            session.add(new_town)
            session.commit()
        except exc.IntegrityError:
            session.rollback()
            return jsonify({'message': 'Duplicate value', 'data': None, 'status': 'error'}), 400
    return jsonify({'message': None, 'data': None, 'status': 'success'}), 201


@towns.route('/api_v1.0/get_towns', methods=['GET'])
def api_get_towns():
    query = session.query(Town)
    if 'id_country' in request.args:
        query.filter(Town.id_country == request.args['id_country'])
    return_data = [map_town(town) for town in query]
    return jsonify({'message': None, 'data': return_data, 'status': 'success'}), 200
