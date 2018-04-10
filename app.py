#!/usr/bin/env python3
import logging
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from model import Base
from gevent.monkey import patch_all
from psycogreen.gevent import patch_psycopg


app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
db.engine.pool._use_threadlocal = True
session = db.session
# patch_all()
# patch_psycopg()


# def get_env_variable(name):
#     try:
#         return os.environ[name]
#     except KeyError:
#         message = "Expected environment variable '{}' not set.".format(name)
#         raise Exception(message)
#
#
# POSTGRES_URL = get_env_variable("POSTGRES_URL")
# POSTGRES_USER = get_env_variable("POSTGRES_USER")
# POSTGRES_PW = get_env_variable("POSTGRES_PW")
# POSTGRES_DB = get_env_variable("POSTGRES_DB")
#
# DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,
#                                                       pw=POSTGRES_PW,
#                                                       url=POSTGRES_URL,
#                                                       db=POSTGRES_DB)


# app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning
# app.config['JSON_AS_ASCII'] = False
# app.config['SECRET_KEY'] =
# app.config['UPLOAD_FOLDER'] = "/home/alex/tmp/img"


# engine = create_engine(DB_URL)
#
# Session = sessionmaker(engine)

# Base.metadata.create_all(engine)

from views import *

if __name__ == '__main__':
    hdlr = logging.FileHandler('log/api_sights.log')
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.info)
    log.addHandler(hdlr)
    # log.addHandler(logging.StreamHandler(sys.stdout))

    if len(sys.argv) == 2:
        host = sys.argv[1]
    else:
        host = '127.0.0.1'
    app.run(host=host)
