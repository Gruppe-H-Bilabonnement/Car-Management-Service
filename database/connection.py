import sqlite3
import os
#from dotenv import load_dotenv

#load_dotenv()

#SQLITE_DB_PATH = os.getenv("car_management.db")

# Create or connect to SQLite database
def create_connection():
    connection = sqlite3.connect('car_management.db')
    connection.row_factory = sqlite3.Row  # Rows as dictionaries
    return connection
