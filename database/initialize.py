import os
import sqlite3
import pandas as pd
from database.connection import create_connection


# Initialize database
def init_db():
    _create_fuel_types_table()
    _create_car_management_table()

    # Check if the car_management table has data
    if not _check_table_data_exists():
        _load_car_data()
        print("Car data loaded successfully")
    else:
        print("Car data already loaded")


# Create car_management table
def _create_car_management_table():
    try:
        connection = create_connection()
        cursor = connection.cursor()

        # Define the table schema
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS car_management (
                id INTEGER PRIMARY KEY,
                purchase_date DATE NOT NULL,
                purchase_price FLOAT NOT NULL,
                car_make TEXT NOT NULL,
                fuel_type_id INTEGER NOT NULL,
                pickup_location TEXT NOT NULL,
                FOREIGN KEY (fuel_type_id) REFERENCES fuel_types(fuel_type_id)
            )
            """
        )

        # Index for faster querying
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_car_make ON car_management (car_make)
            """
        )

    except sqlite3.Error as error:
        print(f"Error creating car_management table: {error}")

    finally:
        connection.commit()
        connection.close()


# Create fuel_types table
def _create_fuel_types_table():
    try:
        connection = create_connection()
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
        connection = create_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) AS count FROM car_management")
        result = cursor.fetchone()[0] > 0
    except sqlite3.Error as error:
        print(f"Error checking if table has data: {error}")
        result = False
    finally:
        connection.close()
        return result


# Load car data from Excel
def _load_car_data():
    # Define the Excel file path
    car_data_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../xlxs/Bilabonnement_2024_Clean.xlsx')
    )

    try:
        # Check if the file exists
        if not os.path.exists(car_data_path):
            print(f"File not found: {car_data_path}")
            return

        # Read relevant columns from Excel
        relevant_columns = {
            "Dato Indkoeb": "purchase_date",
            "Indkoebspris": "purchase_price",
            "Bilmaerke": "car_make",
            "Braendstof": "fuel_type_name",
            "Udleveringssted": "pickup_location",
        }
        data = pd.read_excel(car_data_path, usecols=relevant_columns.keys()).rename(columns=relevant_columns)

        # Convert purchase_date to string in YYYY-MM-DD format
        data["purchase_date"] = data["purchase_date"].dt.strftime("%Y-%m-%d")

        # Normalize fuel_type_name to match database entries
        data["fuel_type_name"] = data["fuel_type_name"].str.strip().str.capitalize()

        # Establish database connection
        connection = create_connection()
        cursor = connection.cursor()

        # Fetch all fuel types into a mapping dictionary
        cursor.execute("SELECT fuel_type_name, fuel_type_id FROM fuel_types")
        fuel_type_mapping = {row[0]: row[1] for row in cursor.fetchall()}

        # Map fuel_type_name to fuel_type_id
        data["fuel_type_id"] = data["fuel_type_name"].map(fuel_type_mapping)

        # Check for unmapped fuel types
        if data["fuel_type_id"].isnull().any():
            unmapped = data[data["fuel_type_id"].isnull()]["fuel_type_name"].unique()
            print(f"Error: Unmapped fuel types found: {unmapped}")
            return

        # Debug: Print a sample of the processed data
        print(data.head())
        #TODO remove this line maybe?

        # Prepare data for insertion
        car_data = data[["purchase_date", "purchase_price", "car_make", "fuel_type_id", "pickup_location"]].values.tolist()

        # Debug: Print number of rows to be inserted
        print(f"Inserting {len(car_data)} rows into car_management...")
        #TODO remove this line maybe?

        # Insert data into car_management
        cursor.executemany(
            """
            INSERT INTO car_management (purchase_date, purchase_price, car_make, fuel_type_id, pickup_location)
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

