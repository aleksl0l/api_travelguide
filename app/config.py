import os

SECRET_KEY = os.environ.get('SECRET_KEY')
SECRET_KEY = 'N1o2o3b4'
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_DATABASE_URI = 'postgresql://travel:travel@localhost/travel'

SQLALCHEMY_TRACK_MODIFICATIONS = False
