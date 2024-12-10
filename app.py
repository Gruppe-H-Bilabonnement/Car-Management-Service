from flask import Flask, jsonify, request
import os
from database.initialize import init_db
from api.routes import car_management_routes
from swagger.config import init_swagger
from flasgger import swag_from

# Initialize Flask app
app = Flask(__name__)

# Initialize database
init_db()

# Initialize Swagger
swagger = init_swagger(app)

# Register the car_management_routes 
app.register_blueprint(car_management_routes, url_prefix='/api/v1/car-management')

# Home route with API documentation for Car Management
@app.route('/api/v1/', methods=['GET'])
def home():
    return jsonify({
        "message": "Welcome to Car Management API",
        "endpoints": [
            {
                "method": "GET",
                "endpoint": "/api/v1/",
                "description": "Provides an overview of the API and its endpoints"
            },
            {
                "method": "GET",
                "endpoint": "/api/v1/car-management/all",
                "description": "Retrieve all cars"
            },
            {
                "method": "GET",
                "endpoint": "/api/v1/car-management/car/<int:id>",
                "description": "Retrieve a car by its ID"
            },
            {
                "method": "GET",
                "endpoint": "/api/v1/car-management/car/make/<int:car_make_id>",
                "description": "Retrieve cars by car make ID"
            },
            {
                "method": "GET",
                "endpoint": "/api/v1/car-management/car/fuel/<int:fuel_type_id>",
                "description": "Retrieve cars by fuel type ID"
            },
            {
                "method": "GET",
                "endpoint": "/api/v1/car-management/car/location/<int:pickup_location_id>",
                "description": "Retrieve cars by pickup location ID"
            },
            {
                "method": "POST",
                "endpoint": "/api/v1/car-management/car",
                "description": "Add a new car"
            },
            {
                "method": "DELETE",
                "endpoint": "/api/v1/car-management/car/<int:id>",
                "description": "Remove a car by ID"
            },
            {
                "method": "PATCH",
                "endpoint": "/api/v1/car-management/car/<int:id>",
                "description": "Update pickup location of a car"
            }
        ]
    })



# Error handler for 404 not found
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

# Error handler for 500 internal server error
@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Init database and run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)