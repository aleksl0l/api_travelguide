from flask import Blueprint, request, jsonify
from app.countries.models import Country
from app.app import session, app
from sqlalchemy import exc

countries = Blueprint('countries', __name__)


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