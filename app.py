from flask import Flask, jsonify, request
import os
from database.initialize import init_db
from api.routes import car_management_routes
from swagger.config import init_swagger
app = Flask(__name__)




# Register the car_management_routes 
app.register_blueprint(car_management_routes, url_prefix='/api/v1/car-management')

swagger = init_swagger(app)


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
    init_db()
    app.run(host='0.0.0.0', port=80)