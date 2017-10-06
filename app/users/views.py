import os
import jwt
import datetime

from flask import Flask, jsonify, request, session, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from . import users
from .. import db, models
from json import dumps

@users.route('/api/user', methods = ['POST'])
def add_new_user():
    json_data = request.get_json()
    password_hash = generate_password_hash(json_data['password'])
    user = User(first_name = json_data['first_name'],
                last_name = json_data['last_name'],
                email = json_data['email'],
                password = password_hash)
    
    try:
        db.session.add(user)
        db.session.commit()
        message = 'Successfully signed up'
    except:
        message = ({"message":"User already taken"})
    db.session.close()
    return jsonify({'message':message})
@users.route('/api/user', methods = ['GET'])
def get_users():
    users = User.query.all()
    all_users = []
    for user in users:
        user_info = {}
        user_info['first_name'] = user.first_name
        user_info['last_name'] = user.last_name
        user_info['email'] = user.email
        user_info['password'] = user.password
        all_users.append(user_info)

    return jsonify({'user':all_users})
@users.route('/api/user/<email>', methods = ['GET'])
def get_user(email):
    user = User.query.filter_by(email = email).first()
    if user:
        user_info = {}
        user_info['first_name'] = user.first_name
        user_info['last_name'] = user.last_name
        user_info['email'] = user.email
        user_info['password'] = user.password
        return jsonify({'user':user_info})

@users.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response(("you need to authorize error 1"),401)
    user = User.query.filter_by(email=auth.username).first()
    if not user:
        return make_response(("you need to authorize error 2"),401)
    
    if check_password_hash(user.password,auth.password):
        token = jwt.encode({'user_id':user.id, 'expiry':dumps(datetime.datetime.utcnow() + datetime.timedelta(minutes=45),default = json_serial)}, os.urandom(64))

        return jsonify({'token':token.decode('UTF-8')})
    make_response(("you need to authorize error 3"),401)


@users.route('/api/user', methods = ['POST'])
def logout():
    session.pop('logged_in', None)
    return jsonify({'message':'successfully logged out'})
    
