from flask import Blueprint, request, jsonify
from app.towns.models import Town
from app.app import session
from sqlalchemy import exc

towns = Blueprint('towns', __name__)


@towns.route('/api_v1.0/create_town', methods=['GET', 'POST'])
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


@towns.route('/api_v1.0/get_towns', methods=['GET', 'POST'])
def api_get_towns():
    d = {}
    q = session.query(Town)
    if 'id_country' in request.args:
        q.filter(Town.id_country == request.args['id_country'])
    for i, town in enumerate(q):
        d[i] = {'id_town': town.id_town,
                'name': town.name,
                'description': town.description,
                'url_photo': town.url_photo
                }
    return jsonify({'message': None, 'data': d, 'status': 'success'})