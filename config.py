import os
DEBUGING = True

BASEDIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///'\
    +os.path.join(BASEDIR, 'api_db.db')

SQLALCHEMY_TRACK_MODIFICATIONS = False
