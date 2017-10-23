import os#pragma:no cover
DEBUGING = True

BASEDIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(BASEDIR, 'db.db')

SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY="\xf9'\xe4p(\xa9\x12\x1a!\x94\x8d\x1c\x99l\xc7\xb7e\xc7c\x86\x02MJ\xa0"
