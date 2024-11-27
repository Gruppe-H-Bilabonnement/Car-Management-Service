import sqlite3
from database.connection import create_connection


# Retrieve all cars
def retrieve_all_cars():
    try:
        connection = create_connection()
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