import os
import jwt
import datetime
from flask import Flask, jsonify, request, session, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from . import users
from app import app, db, models
from json import dumps

def token_required(funct):
    @wraps(funct)
    def decorated_funct(*args, **kwargs):
        token = None
        if 'x_access_token' in request.headers:
            token = request.headers['x_access_token']
            if not token:
                return jsonify({"message":"Token is missing"}), 401
            try:
                data = jwt.decode(token, app.config['SECRET_KEY'])
                current_user = models.User.query.filter_by(id=data["sub"]).first()
            except:
                return jsonify({"message":"Token is invalid"}), 401
            return funct(current_user, *args, **kwargs)
    return decorated_funct

@users.route('/api/user', methods = ['POST'])
def add_new_user():
    json_data = request.get_json()
    user = models.User(first_name = json_data['first_name'],
                last_name = json_data['last_name'],
                email = json_data['email'],
                password = generate_password_hash(json_data['password']))
    
    try:
        db.session.add(user)
        db.session.commit()
        message = 'Successfully signed up'
    except:
        message = 'User already taken'
    db.session.close()
    return jsonify({'message':message})
@users.route('/api/user', methods = ['GET'])
def get_users():
    users = models.User.query.all()
    all_users = []
    for user in users:
        user_info = {}
        user_info['id'] = user.id
        user_info['first_name'] = user.first_name
        user_info['last_name'] = user.last_name
        user_info['email'] = user.email
        user_info['password'] = user.password
        all_users.append(user_info)

    return jsonify({'users':all_users})

@users.route('/api/user/<email>', methods = ['GET'])
def get_user(email):
    user = models.User.query.filter_by(email=email).first()
    if user:
        user_info = {}
        user_info['id']= user.id
        user_info['first_name'] = user.first_name
        user_info['last_name'] = user.last_name
        user_info['email'] = user.email
        user_info['password'] = user.password
        return jsonify({'user':user_info})
    return jsonify({'message':'No user found'})

@users.route('/login', methods = ['POST'])
def login():
    auth = request.get_json()

    if not auth or not auth['email'] or not auth['password']:
        return make_response(("you need to authorize with email and password"),401)
    user = models.User.query.filter_by(email=auth['email']).first()
    if not user:
        return make_response(("you need to use a correct email"),401)
    
    if check_password_hash(user.password,auth['password']):
        token = jwt.encode({
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=45),
            'iat': datetime.datetime.utcnow(),
            'sub': user.id},app.config.get('SECRET_KEY'), algorithm='HS256')

        return jsonify({'token':token})
    return make_response(("you need to authorize with correct password"),401)
    
