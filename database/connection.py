import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

SQLITE_DB_PATH = os.getenv("/home/car_management.db")

# Create or connect to SQLite database
def create_connection():
    connection = sqlite3.connect('SQLite_DB_PATH')
    connection.row_factory = sqlite3.Row  # Rows as dictionaries
    return connection
