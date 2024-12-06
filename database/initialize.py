import os
import sqlite3
import pandas as pd
from dotenv import load_dotenv

# Load envoirnment variables
load_dotenv()

SQLITE_DB_PATH = os.getenv('SQLITE_DB_PATH', 'car_management.db')

# Initialize database
def init_db():
    # Create tables if they do not exist
    _create_fuel_types_table()
    _create_car_make_table()
    _create_pickup_location_table()
    _create_car_management_table()
    
    if not _check_table_data_exists():
        _load_car_data()
        print("Car data loaded successfully")
    else:
        print("Car data already loaded")


# Create car_management table
def _create_car_management_table():
    try:
        connection = sqlite3.connect(SQLITE_DB_PATH)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        # Define the car_management table schema
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS car_management (
                id INTEGER PRIMARY KEY,
                purchase_date DATE NOT NULL,
                purchase_price FLOAT NOT NULL,
                car_make_id INTEGER NOT NULL,
                fuel_type_id INTEGER NOT NULL,
                pickup_location_id INTEGER NOT NULL,
                FOREIGN KEY (car_make_id) REFERENCES car_make(car_make_id),
                FOREIGN KEY (fuel_type_id) REFERENCES fuel_types(fuel_type_id),
                FOREIGN KEY (pickup_location_id) REFERENCES pickup_location(pickup_location_id)
            )
            """
        )
    except sqlite3.Error as error:
        print(f"Error creating car_management table: {error}")
    finally:
        connection.commit()
        connection.close()


# Create car_make table
def _create_car_make_table():
    try:
        connection = sqlite3.connect(SQLITE_DB_PATH)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        # Define the car_make table schema
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS car_make (
                car_make_id INTEGER PRIMARY KEY,
                car_make_name TEXT NOT NULL UNIQUE
            )
            """
        )
    except sqlite3.Error as error:
        print(f"Error creating car_make table: {error}")
    finally:
        connection.commit()
        connection.close()


# Create pickup_location table
def _create_pickup_location_table():
    try:
        connection = sqlite3.connect(SQLITE_DB_PATH)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        # Define the pickup_location table schema
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS pickup_location (
                pickup_location_id INTEGER PRIMARY KEY,
                pickup_location_name TEXT NOT NULL UNIQUE
            )
            """
        )
    except sqlite3.Error as error:
        print(f"Error creating pickup_location table: {error}")
    finally:
        connection.commit()
        connection.close()


# Create fuel_types table
def _create_fuel_types_table():
    try:
        connection = sqlite3.connect(SQLITE_DB_PATH)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        # Define the fuel_types table schema
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS fuel_types (
                fuel_type_id INTEGER PRIMARY KEY,
                fuel_type_name TEXT NOT NULL UNIQUE
            )
            """
        )

        # Insert predefined fuel types if the table is empty
        cursor.execute("SELECT COUNT(*) FROM fuel_types")
        if cursor.fetchone()[0] == 0:
            fuel_types = [
                (1, "Benzin"),
                (2, "Diesel"),
                (3, "Elektrisk"),
                (4, "Hybrid"),
            ]
            cursor.executemany(
                "INSERT INTO fuel_types (fuel_type_id, fuel_type_name) VALUES (?, ?)", fuel_types
            )

    except sqlite3.Error as error:
        print(f"Error creating or populating fuel_types table: {error}")

    finally:
        connection.commit()
        connection.close()


# Check if car_management has data
def _check_table_data_exists():
    try:
        connection = sqlite3.connect(SQLITE_DB_PATH)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) AS count FROM car_management")
        result = cursor.fetchone()[0] > 0
    except sqlite3.Error as error:
        print(f"Error checking if table has data: {error}")
        result = False
    finally:
        connection.close()
        return result


# Load car data from CSV
def _load_car_data():
    # Define the CSV file path
    car_data_path = os.path.join(os.path.dirname(__file__), '../csv/Bilabonnement_2024_Clean.csv')

    try:
        # Check if the file exists
        if not os.path.exists(car_data_path):
            print(f"File not found: {car_data_path}")
            return

        # Read relevant columns from CSV
        relevant_columns = {
            "Dato Indkoeb": "purchase_date",
            "Indkoebspris": "purchase_price",
            "Bilmaerke": "car_make_name",
            "Braendstof": "fuel_type_name",
            "Udleveringssted": "pickup_location_name",
        }
        data = pd.read_csv(car_data_path, usecols=relevant_columns.keys()).rename(columns=relevant_columns)
        
        # Convert purchase_date to string in YYYY-MM-DD format
        data["purchase_date"] = pd.to_datetime(data["purchase_date"]).dt.strftime("%Y-%m-%d")

        # Normalize strings
        data["fuel_type_name"] = data["fuel_type_name"].str.strip().str.capitalize()
        data["car_make_name"] = data["car_make_name"].str.strip().str.capitalize()
        data["pickup_location_name"] = data["pickup_location_name"].str.strip().str.capitalize()

        # Establish database connection
        connection = sqlite3.connect(SQLITE_DB_PATH)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        # Insert unique car makes into car_make table and create a mapping
        car_make_mapping = _populate_mapping_table(cursor, "car_make", "car_make_id", "car_make_name", data["car_make_name"])

        # Insert unique pickup locations into pickup_location table and create a mapping
        pickup_location_mapping = _populate_mapping_table(cursor, "pickup_location", "pickup_location_id", "pickup_location_name", data["pickup_location_name"])

        # Fetch all fuel types into a mapping dictionary
        cursor.execute("SELECT fuel_type_name, fuel_type_id FROM fuel_types")
        fuel_type_mapping = {row[0]: row[1] for row in cursor.fetchall()}

        # Map names to IDs
        data["car_make_id"] = data["car_make_name"].map(car_make_mapping)
        data["pickup_location_id"] = data["pickup_location_name"].map(pickup_location_mapping)
        data["fuel_type_id"] = data["fuel_type_name"].map(fuel_type_mapping)

        # Check for unmapped data
        for column in ["car_make_id", "pickup_location_id", "fuel_type_id"]:
            if data[column].isnull().any():
                unmapped = data[data[column].isnull()]
                print(f"Error: Unmapped values found in {column}: {unmapped}")
                return

        # Prepare data for insertion
        car_data = data[["purchase_date", "purchase_price", "car_make_id", "fuel_type_id", "pickup_location_id"]].values.tolist()

        # Debug: Print number of rows to be inserted
        print(f"Inserting {len(car_data)} rows into car_management...")

        # Insert data into car_management
        cursor.executemany(
            """
            INSERT INTO car_management (purchase_date, purchase_price, car_make_id, fuel_type_id, pickup_location_id)
            VALUES (?, ?, ?, ?, ?)
            """,
            car_data
        )

    except sqlite3.Error as error:
        print(f"Error loading car data: {error}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        connection.commit()
        connection.close()


def _populate_mapping_table(cursor, table_name, id_column, name_column, values):
    """
    Populates a mapping table with unique values and returns a dictionary of name-to-id mappings.
    """
    cursor.executemany(
        f"INSERT OR IGNORE INTO {table_name} ({name_column}) VALUES (?)",
        [(value,) for value in values.unique()]
    )

    # Fetch the mappings
    cursor.execute(f"SELECT {name_column}, {id_column} FROM {table_name}")
    return {row[0]: row[1] for row in cursor.fetchall()}
