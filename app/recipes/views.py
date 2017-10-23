from flask import Flask, jsonify, request, session, make_response#pragma:no cover
from app.models import Recipe#pragma:no cover
from app.users.views import token_required#pragma:no cover
from . import recipes#pragma:no cover
from .. import db, models#pragma:no cover

@recipes.route('/api/recipe', methods = ['POST'])
@token_required
def add_new_recipe(current_user):
    json_data = request.get_json()
    recipe = Recipe(name = json_data['name'],
                description = json_data['description'])
    
    try:
        db.session.add(recipe)
        db.session.commit()
        message = 'Successfully added recipe'
    except:
        message = 'An error occured try again'
    db.session.close()
    return jsonify({'message':message})

@recipes.route('/api/recipe', methods = ['GET'])
def get_recipe_list():
    recipes = Recipe.query.all()
    all_recipes = []
    for recipe in recipes:
        rec_data = {}
        rec_data['name'] = recipe.name
        rec_data['description'] = recipe.description
        all_recipes.append(rec_data)

    return jsonify({'recipe':all_recipes})

@recipes.route('/api/recipe/<name>', methods = ['GET'])
def get_recipe(name):
    json_data= request.get_json()
    recipe = Recipe.query.filter_by(name=json_data['name']).first()
    if recipe:
        rec_data = {}
        rec_data['name'] = recipe.name
        rec_data['description'] = recipe.description
        return jsonify({'recipe':rec_data})
    return jsonify({"message":"recipe does not exist"})

@recipes.route('/api/recipe/<name>', methods = ['PUT'])
@token_required
def edit_recipe(current_user, name):
    json_data= request.get_json()
    recipe = Recipe.query.filter_by(name=json_data['name']).first()
    if not recipe:
        return jsonify({"Message":"Recipe non exitent"}), 401

    recipe = Recipe(name = json_data['new_name'],
                    description = json_data['new_description'])

    return jsonify({'message':'Successfully edited'})

@recipes.route('/api/recipe/<name>', methods = ['DELETE'])
@token_required
def delete_recipe(current_user, name):
    json_data= request.get_json()
    recipe = Recipe.query.filter_by(name=json_data['name']).first()
    if not recipe:
        return jsonify({"message":"Recipe does not exist"})
    db.session.delete(recipe)
    db.session.commit()
    return jsonify({"message":"successfully deleted"})
