from flask import Blueprint, jsonify, request
from flasgger import swag_from
from repositories.repository import (
    db_retrieve_all_cars,
    db_retrieve_car_by_id,
    db_retrieve_car_by_make,
    db_retrieve_car_by_fuel_type,
    db_retrieve_car_by_pickup_location,
    db_add_new_car,
    db_remove_car_by_id,
    db_update_pickup_location
    )

car_management_routes = Blueprint('car_management_routes', __name__)


# Get all cars
@car_management_routes.route('/all', methods=['GET'])
@swag_from('../swagger/docs/get_all_cars.yml')
def get_all_cars():
    try:
        cars = db_retrieve_all_cars()
        return jsonify(cars), 200
    except Exception as error:
        return jsonify({'error': str(error)}), 500
    

# Retrieve a car by ID
@car_management_routes.route('/car/<int:id>', methods=['GET'])
def get_car_by_id(id):
    try:
        car = db_retrieve_car_by_id(id)
        if car:
            return jsonify(car), 200
        else:
            return jsonify({'error': 'Car not found'}), 404
    except Exception as error:
        return jsonify({'error': str(error)}), 500

# Retrieve cars by make
@car_management_routes.route('/car/make/<int:car_make_id>', methods=['GET'])
def get_cars_by_make(car_make_id):
    try:
        cars = db_retrieve_car_by_make(car_make_id)
        if cars:
            return jsonify(cars), 200
        else:
            return jsonify({'error': 'No cars found for the given make'}), 404
    except Exception as error:
        return jsonify({'error': str(error)}), 500

# Retrieve cars by fuel type
@car_management_routes.route('/car/fuel/<int:fuel_type_id>', methods=['GET'])
def get_cars_by_fuel_type(fuel_type_id):
    try:
        cars = db_retrieve_car_by_fuel_type(fuel_type_id)
        if cars:
            return jsonify(cars), 200
        else:
            return jsonify({'error': 'No cars found for the given fuel type'}), 404
    except Exception as error:
        return jsonify({'error': str(error)}), 500

# Retrieve cars by pickup location
@car_management_routes.route('/car/location/<int:pickup_location_id>', methods=['GET'])
def get_cars_by_pickup_location(pickup_location_id):
    try:
        cars = db_retrieve_car_by_pickup_location(pickup_location_id)
        if cars:
            return jsonify(cars), 200
        else:
            return jsonify({'error': 'No cars found for the given pickup location'}), 404
    except Exception as error:
        return jsonify({'error': str(error)}), 500

# Add a new car
@car_management_routes.route('/car', methods=['POST'])
def add_car():
    try:
        data = request.get_json()
        message = db_add_new_car(data)
        return jsonify({'message': message}), 201
    except Exception as error:
        return jsonify({'error': str(error)}), 500
    
# Remove a car by id
@car_management_routes.route('/car/<int:id>', methods=['DELETE'])
def delete_car(id):
    try:
        message = db_remove_car_by_id(id)
        return jsonify({'message': message}), 200
    except Exception as error:
        return jsonify({'error': str(error)}), 500

# Update pickup location of a car
@car_management_routes.route('/car/<int:id>', methods=['PATCH'])
def update_car_location(id):
    try:
        data = request.get_json()
        message = db_update_pickup_location(id, data)
        return jsonify({'message': message}), 200
    except Exception as error:
        return jsonify({'error': str(error)}), 500
