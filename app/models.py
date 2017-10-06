from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    email = db.Column(db.String(60), unique=True)
    password = db.Column(db.String(300))
    category_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        
    
class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    user = db.relationship('User', backref='recipes',
                                 lazy='dynamic')
    def __init__(self, name, description):
        self.name = name
        self.description = description

    #create engine to store data in local non-persistent database directory   

db.Model.metadata.bind = create_engine('sqlite:///api_db.db')
db.create_all()
