from sqlalchemy import Column, ForeignKey, Integer, String#pragma:no cover
from sqlalchemy import create_engine#pragma:no cover
from sqlalchemy.orm import relationship#pragma:no cover
from app import db#pragma:no cover


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    email = db.Column(db.String(60), unique=True)
    password = db.Column(db.String(300))
    category_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name#pragma:no cover
        self.last_name = last_name#pragma:no cover
        self.email = email#pragma:no cover
        self.password = password#pragma:no cover
        db.create_all()   #pragma:no cover
    
class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    description = db.Column(db.String(1000), nullable=False)
    user = db.relationship('User', backref='recipes',
                                 lazy='dynamic')
    def __init__(self, name, description):
        self.name = name#pragma:no cover
        self.description = description#pragma:no cover
        db.create_all()#pragma:no cover


