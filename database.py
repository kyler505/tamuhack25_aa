# database.py
import sqlite3
import json
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import random

# Database file name
DATABASE = 'users.db'

def init_db():
    """Initialize the database and create the tables if they don't exist."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        
        # Create the users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                past_flights TEXT
            )
        ''')
        
        # Create the airline_data table for past flights
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS airline_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                flight_time TEXT NOT NULL,
                price REAL NOT NULL,
                distance REAL NOT NULL
            )
        ''')
        
        conn.commit()

def add_user(username, password, past_flights=None):
    """Add a new user to the database."""
    password_hash = generate_password_hash(password)
    # Serialize past_flights to JSON if it exists
    past_flights_json = json.dumps(past_flights) if past_flights else None
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (username, password_hash, past_flights)
                VALUES (?, ?, ?)
            ''', (username, password_hash, past_flights_json))
            conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Username already exists
        return False

def verify_user(username, password):
    """Verify if the username and password match a user in the database."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT password_hash FROM users WHERE username = ?
        ''', (username,))
        result = cursor.fetchone()
        if result and check_password_hash(result[0], password):
            return True
    return False

def user_exists(username):
    """Check if a user exists in the database."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id FROM users WHERE username = ?
        ''', (username,))
        return cursor.fetchone() is not None

def special_filter(username, origin, destination):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        # filter out fllights that do not fit within the trend given by the cluster analysis
        cursor.execute('''SELECT * FROM flight_data WHERE price < 500 AND origin = ? AND destination = ?''', (origin, destination))

def get_user_data(username):
    """Fetch a user's data from the users table."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT username, past_flights FROM users WHERE username = ?
        ''', (username,))
        result = cursor.fetchone()
        if result:
            return {
                "username": result[0],
                "past_flights": json.loads(result[1]) if result[1] else []
            }
    return None   
    
def add_aa_flight(flight_time, price, distance):
    """Add a flight to the airline_data table."""
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO airline_data (flight_time, price, distance)
                VALUES (?, ?, ?)
            ''', (flight_time, price, distance))
            conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Handle duplicate flights or other integrity errors
        return False

# clears the airline table
def clear_airline_data():
    """Delete all rows from the airline_data table."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM airline_data')
        conn.commit()
        print("Cleared airline_data table.")

# # remove and add new users
def delete_all_users():
    """Delete all rows from the users table."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users')
        conn.commit()
        print("All users deleted successfully.")

# def add_past_flights_column():
#     """Add the past_flights column to the users table."""
#     with sqlite3.connect(DATABASE) as conn:
#         cursor = conn.cursor()
#         # Check if the column already exists
#         cursor.execute("PRAGMA table_info(users)")
#         columns = [column[1] for column in cursor.fetchall()]
#         if 'past_flights' not in columns:
#             # Add the past_flights column
#             cursor.execute('ALTER TABLE users ADD COLUMN past_flights TEXT')
#             conn.commit()
#             print("Added past_flights column to the users table.")
#         else:
#             print("past_flights column already exists.")
