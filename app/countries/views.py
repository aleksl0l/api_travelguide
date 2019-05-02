from flask import Blueprint, request, jsonify
from sqlalchemy import exc

from app.app import session
from app.countries.models import Country

countries = Blueprint('countries', __name__)


@countries.route('/api_v1.0/create_country', methods=['POST'])
def api_create_country():
    print(request.args)
    if 'name' in request.args:
        new_count = Country(name=request.args['name'])
        try:
            session.add(new_count)
            session.commit()
        except exc.IntegrityError:
            session.rollback()
            return jsonify({'message': 'Duplicate value', 'data': None, 'status': 'error'}), 400
    return jsonify({'message': None, 'data': None, 'status': 'success'}), 200


@countries.route('/api_v1.0/get_countries', methods=['GET'])
def api_get_countries():
    q = session.query(Country)
    if 'id_country' in request.args:
        q = q.filter(Country.id_country == request.args['id_country'])
    response_data = [country.serialize() for country in q]
    return jsonify({'message': None, 'data': response_data, 'status': 'success'}), 200
