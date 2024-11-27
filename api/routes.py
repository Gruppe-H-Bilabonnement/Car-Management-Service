from flask import Blueprint, jsonify, request
from flasgger import swag_from
from repositories.repository import retrieve_all_cars

car_management_routes = Blueprint('car_management_routes', __name__)

@car_management_routes.route('/all', methods=['GET'])
@swag_from('../swagger/docs/get_all_cars.yml')
def get_all_cars():
    try:
        cars = retrieve_all_cars()
        return jsonify(cars), 200
    except Exception as error:
        return jsonify({'error': str(error)}), 500
