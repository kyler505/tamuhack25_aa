# database.py
import sqlite3
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
                password_hash TEXT NOT NULL
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

def add_user(username, password):
    """Add a new user to the database."""
    password_hash = generate_password_hash(password)
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (username, password_hash)
                VALUES (?, ?)
            ''', (username, password_hash))
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

def get_user_details(username):
    """Fetch user details from the database."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT username FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        if user:
            return {
                'username': user[0]
            }
        return None

def insert_mock_flight_data():
    """Insert mock data for past flights into the airline_data table."""
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"]
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        for _ in range(20):  # Insert 20 mock flights
            flight_number = f"AA{random.randint(100, 999)}"
            departure_city = random.choice(cities)
            destination_city = random.choice([city for city in cities if city != departure_city])
            departure_time = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d %H:%M:%S")
            arrival_time = (datetime.now() - timedelta(days=random.randint(1, 30)) + timedelta(hours=random.randint(1, 6))).strftime("%Y-%m-%d %H:%M:%S")
            price = round(random.uniform(100, 500), 2)
            distance = round(random.uniform(500, 2000), 2)
            
            cursor.execute('''
                INSERT INTO airline_data (flight_number, departure_city, destination_city, departure_time, arrival_time, price, distance)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (flight_number, departure_city, destination_city, departure_time, arrival_time, price, distance))
        conn.commit()

def get_past_flights():
    """Fetch all past flights from the airline_data table."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM airline_data')
        flights = cursor.fetchall()
        return [
            {
                'id': flight[0],
                'flight_number': flight[1],
                'departure_city': flight[2],
                'destination_city': flight[3],
                'departure_time': flight[4],
                'arrival_time': flight[5],
                'price': flight[6],
                'distance': flight[7]
            }
            for flight in flights
        ]