#!/usr/bin/env python3
from flask import request, Flask, jsonify, Response
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc
from model import db, Country, Town, Sights, Base

app = Flask(__name__)


def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)


POSTGRES_URL = get_env_variable("POSTGRES_URL")
POSTGRES_USER = get_env_variable("POSTGRES_USER")
POSTGRES_PW = get_env_variable("POSTGRES_PW")
POSTGRES_DB = get_env_variable("POSTGRES_DB")

DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,
                                                      pw=POSTGRES_PW,
                                                      url=POSTGRES_URL,
                                                      db=POSTGRES_DB)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning
app.config['JSON_AS_ASCII'] = False
engine = create_engine(DB_URL)
db.init_app(app)

Session = sessionmaker(engine)
session = Session()
Base.metadata.create_all(engine)


@app.route('/api_v1.0')
def api_root():
    return ')'


@app.route('/api_v1.0/create_country')
def api_create_country():
    print(request.args)
    if 'name' in request.args:
        new_count = Country(name=request.args['name'])
        try:
            session.add(new_count)
            session.commit()
        except exc.IntegrityError:
            session.rollback()
            return jsonify({"success": False})
    return jsonify({"success": True})


@app.route('/api_v1.0/get_countries')
def api_get_countries():
    d = {}
    q = session.query(Country)
    if 'id_country' in request.args:
        q = q.filter(Country.id_country == request.args['id_country'])
    for i, country in enumerate(q):
        d[i] = {'id_town': country.id_country, 'name': country.name}
    return jsonify(d)


@app.route('/api_v1.0/create_town')
def api_create_town():
    print(request.args)
    if 'name' in request.args:
        try:
            new_town = Town(name=request.args['name'], id_country=2)
            session.add(new_town)
            session.commit()
        except exc.IntegrityError:
            session.rollback()
            return jsonify({"success": False})
    return jsonify({"success": True})


@app.route('/api_v1.0/get_towns')
def api_get_towns():
    d = {}
    q = session.query(Town)
    if 'id_country' in request.args:
        q.filter(Town.id_country == request.args['id_country'])
    for i, town in enumerate(q):
        d[i] = {'id_town': town.id_town, 'name': town.name, 'description': town.description}
    return jsonify(d)


@app.route('/api_v1.0/create_sight')
def api_create_sights():
    print(request.args)
    if 'id_town' in request.args and 'name' in request.args:
        try:
            new_sight = Sights(id_town=request.args['id_town'], name=request.args['name'])
            session.add(new_sight)
            session.commit()
        except exc.IntegrityError:
            session.rollback()
            return jsonify({"success": False})
        return jsonify({"success": True})


@app.route('/api_v1.0/get_sights')
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
        return jsonify(d)
    else:
        return jsonify({"success": False})


@app.route('/api_v1.0/modify_sight')
def api_modify_sight():
    if 'id_sight' in request.args:
        d = request.args.to_dict(flat=True)
        if 'tag' in d:
            d['tag'] = d['tag'].split(',')
        d.pop('id_sight')
        print(type(d), d)
        session.query(Sights).filter(Sights.id_sights == request.args['id_sight']).update(d)
        session.commit()
        return jsonify(d)
    else:
        return jsonify({"success": False})

if __name__ == '__main__':
    if len(sys.argv) == 2:
        host = sys.argv[1]
    else:
        host = '127.0.0.1'
    app.run(host=host)
