from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config.from_object('config')

db=SQLAlchemy(app)
db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)

from app.users import users as users_blueprint
app.register_blueprint(users_blueprint)
