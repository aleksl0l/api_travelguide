#!/usr/bin/env python3
import logging
import sys

from flask import Flask, jsonify

from app.basemodels import db
from app.countries.views import countries
from app.exceptions import InvalidUsage
from app.likes.views import likes
from app.sights.views import sights
from app.towns.views import towns
from app.users.views import users

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)
db.app = app
db.engine.pool._use_threadlocal = True


app.register_blueprint(likes)
app.register_blueprint(countries)
app.register_blueprint(towns)
app.register_blueprint(sights)
app.register_blueprint(users)

if __name__ == '__main__':
    handler = logging.FileHandler('log/api_sights.log')
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.info)
    log.addHandler(handler)

    if len(sys.argv) == 2:
        host = sys.argv[1]
    else:
        host = '127.0.0.1'
    app.run(host=host)


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
