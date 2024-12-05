import sqlite3
import os
from dotenv import load_dotenv

load_dotenv(override=True)

SQLITE_DB_PATH = os.getenv('SQLITE_DB_PATH', os.path.join(os.environ['HOME'], 'data', 'car_management.db'))

if not os.path.exists(SQLITE_DB_PATH):
    raise FileNotFoundError(f"Database not found at {SQLITE_DB_PATH}")

# Create or connect to SQLite database
def create_connection():
    connection = sqlite3.connect(SQLITE_DB_PATH)
    connection.row_factory = sqlite3.Row  # Rows as dictionaries
    return connection
