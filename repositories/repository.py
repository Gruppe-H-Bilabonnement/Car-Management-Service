import sqlite3
import os
from dotenv import load_dotenv

# Load envoirnment variables
load_dotenv()

SQLITE_DB_PATH = os.getenv('SQLITE_DB_PATH', 'car_management.db')

# Retrieve all cars
def db_retrieve_all_cars():
    try:
        connection = sqlite3.connect(SQLITE_DB_PATH)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        # Retrieve all cars
        cursor.execute(
            """
            SELECT * FROM car_management
            """
        )
        cars = cursor.fetchall()
        return [dict(row) for row in cars]
    except sqlite3.Error as error:
        print(f"Database error: {error}")
    finally:
        connection.close()


# Retrieve a car by id
def db_retrieve_car_by_id(id):
    try:
        connection = sqlite3.connect(SQLITE_DB_PATH)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT * FROM car_management WHERE id = ?
            """, (id,)
        )
        car = cursor.fetchone()
        return dict(car)
    except sqlite3.Error as error:
        print(f"Database error: {error}")
    finally:
        connection.close()

# Retrieve car by make
def db_retrieve_car_by_make(car_make_id):
    try:
        connection = sqlite3.connect(SQLITE_DB_PATH)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT * FROM car_management WHERE car_make_id = ?
            """, (car_make_id,)
        )
        car = cursor.fetchall()
        return [dict(row) for row in car]
    except sqlite3.Error as error:
        print(f"Database error: {error}")
    finally:
        connection.close()

# Retrieve car by fuel type
def db_retrieve_car_by_fuel_type(fuel_type_id):
    try:
        connection = sqlite3.connect(SQLITE_DB_PATH)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT * FROM car_management WHERE fuel_type_id = ?
            """, (fuel_type_id,)
        )
        car = cursor.fetchall()
        return [dict(row) for row in car]
    except sqlite3.Error as error:
        print(f"Database error: {error}")
    finally:
        connection.close()

# Retrieve car by pickup location
def db_retrieve_car_by_pickup_location(pickup_location_id):
    try:
        connection = sqlite3.connect(SQLITE_DB_PATH)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT * FROM car_management WHERE pickup_location_id = ?
            """, (pickup_location_id,)
        )
        car = cursor.fetchall()
        return [dict(row) for row in car]
    except sqlite3.Error as error:
        print(f"Database error: {error}")
    finally:
        connection.close()

# Add a new car
def db_add_new_car(data):
    try:
        connection = sqlite3.connect(SQLITE_DB_PATH)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO car_management (purchase_date, purchase_price, car_make_id, fuel_type_id, pickup_location_id) Values (?, ?, ?, ?, ?)
            """, (
                data['purchase_date'], 
                data['purchase_price'], 
                data['car_make_id'], 
                data['fuel_type_id'], 
                data['pickup_location_id']
                )
        )
        connection.commit()
        return "Car added successfully"
    except sqlite3.Error as error:
        print(f"Database error: {error}")
    finally:
        connection.close()


# Remove a car
def db_remove_car_by_id(id):
    try:
        connection = sqlite3.connect(SQLITE_DB_PATH)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM car_management WHERE id = ?
            """, (id,)
        )
        connection.commit()
        return "Car removed successfully"
    except sqlite3.Error as error:
        print(f"Database error: {error}")
    finally:
        connection.close()

# Update pickup location id using JSON body and id
def db_update_pickup_location(id, data):
    try:
        connection = sqlite3.connect(SQLITE_DB_PATH)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE car_management SET pickup_location_id = ? WHERE id = ?
            """, (data['pickup_location_id'], id)
        )
        connection.commit()
        return "Pickup location updated successfully"
    except sqlite3.Error as error:
        print(f"Database error: {error}")
    finally:
        connection.close()
        