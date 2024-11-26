from flask import Flask, jsonify, request
import os
from database.initialize import init_db

app = Flask(__name__)









if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5001)