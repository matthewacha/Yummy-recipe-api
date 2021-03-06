from flask import Flask
from flask_sqlalchemy import import SQLAlchemy

app=Flask(__name__)
app.config.from_file('config')

db=SQLAlchemy(app)
db.create_all()

from app import views
