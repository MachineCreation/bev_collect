from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Car, car_schema, cars_schema

api = Blueprint('api',__name__, url_prefix='/api')


                                                                                #post contact test route

@api.route('/new_car', methods = ['POST'])
@token_required
def new_car(current_user_token):
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    mileage = request.json['mileage']
    when_purchased = request.json['when_purchased']

    print(f'BIG TESTER: {current_user_token.token}')

    car = Car(make, model, year, mileage,when_purchased, user_token = current_user_token.token)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

                                                                                #retrieve all contacts route

@api.route('/cars', methods = ['GET'])
@token_required
def list_all_cars(current_user_token):
    a_user = current_user_token.token
    cars = Car.query.filter_by(user_token = a_user).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

                                                                                #retrieve single contact route by id

@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_single_car(current_user_token,id):
    car = car.query.get(id) 
    response = car_schema.dump(car)
    return response

                                                                                # update single contact by id

@api.route('/cars/<id>', methods = ['POST','PUT'])
@token_required
def update_car_info(current_user_token,id):
    car = car.query.get(id) 
    car.make = request.json['make']
    car.model = request.json['model']
    car.year = request.json['year']
    car.mileage = request.json['mileage']
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

                                                                                # delete single contact by id

@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)
