import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    # set connection to your DB
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'your_db_uri'
    # or if you want to use sqlite, use next line
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
