# database.py
import sqlite3
import json
from werkzeug.security import generate_password_hash, check_password_hash

# database file name
DATABASE = 'users.db'

def init_db():
    """Initialize the database and create the users table if it doesn't exist."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        # create users info table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
                # new column for past user flight data, to be used for recommendations: price, time depature, distance
                past_flights TEXT
            )
        ''')

        # create airline info table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS airline_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                flight_time REAL NOT NULL,
                price REAL NOT NULL,
                distance REAL NOT NULL
            )
        ''')

        conn.commit()

# user functions
def add_user(username, password, past_flights=None):
    """Add a new user to the database with optional past flight data."""
    password_hash = generate_password_hash(password)
    past_flights_json = json.dumps(past_flights) if past_flights else "[]"  # Serialize to JSON
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

def update_user_past_flights(username, past_flights):
    """Update a user's past flight data."""
    past_flights_json = json.dumps(past_flights)  # Serialize to JSON
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users SET past_flights = ? WHERE username = ?
        ''', (past_flights_json, username))
        conn.commit()
        return True
        
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
    
def get_user_past_flights(username):
    """Retrieve a user's past flight data."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT past_flights FROM users WHERE username = ?
        ''', (username,))
        result = cursor.fetchone()
        if result and result[0]:
            return json.loads(result[0])  # Deserialize JSON
        return []

# functions to add more data to the db
def add_aa_flight(flight_time, price, distance):
    """Add a flight to the database."""
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO flights (flight_time, price, distance)
                VALUES (?, ?, ?)
            ''', (flight_time, price, distance))
            conn.commit()
        return True
    except sqlite3.IntegrityError:
        # handle duplicate flights or other integrity errors
        return False