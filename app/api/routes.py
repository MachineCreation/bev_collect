from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Beverage, beverage_schema, beverages_schema

api = Blueprint('api',__name__, url_prefix='/api')


                                                                                #post contact test route

@api.route('/new_beverage', methods = ['POST'])
@token_required
def new_beverage(current_user_token):
    base_liquor = request.json['base_liquor']
    name = request.json['name']
    glass_type = request.json['glass_type']
    recipe = request.json['recipe']
    comments = request.json['comments']

    print(f'BIG TESTER: {current_user_token.token}')

    beverage = Beverage(base_liquor, name, glass_type, recipe,comments, user_token = current_user_token.token)

    db.session.add(beverage)
    db.session.commit()

    response = beverage_schema.dump(beverage)
    return jsonify(response)

                                                                                #retrieve all contacts route

@api.route('/beverages', methods = ['GET'])
@token_required
def list_all_beverages(current_user_token):
    a_user = current_user_token.token
    beverages = Beverage.query.filter_by(user_token = a_user).all()
    response = beverages_schema.dump(beverages)
    return jsonify(response)

                                                                                #retrieve single contact route by id

@api.route('/beverages/<id>', methods = ['GET'])
@token_required
def get_single_beverage(current_user_token,id):
    beverage = Beverage.query.get(id) 
    response = beverage_schema.dump(beverage)
    return response

                                                                                # update single contact by id

@api.route('/beverages/<id>', methods = ['POST','PUT'])
@token_required
def update_beverage_info(current_user_token,id):
    beverage = Beverage.query.get(id) 
    beverage.base_liquor = request.json['base_liquor']
    beverage.name = request.json['name']
    beverage.glass_type = request.json['glass_type']
    beverage.recipe = request.json['recipe']
    beverage.comments = request.json['comments']
    beverage.user_token = current_user_token.token

    db.session.commit()
    response = beverage_schema.dump(beverage)
    return jsonify(response)

                                                                                # delete single contact by id

@api.route('/beverages/<id>', methods = ['DELETE'])
@token_required
def delete_beverage(current_user_token, id):
    beverage = Beverage.query.get(id)
    db.session.delete(beverage)
    db.session.commit()
    response = beverage_schema.dump(beverage)
    return jsonify(response)
