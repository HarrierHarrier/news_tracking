import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
        b'kD\xf5|\xc7.\x11.o\x0e\xefn\x00\x84\xeb!u\xf7\xb3\xb3\xfc\xffv\xc9'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
