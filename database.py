# database.py
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Database file name
DATABASE = 'users.db'

def init_db():
    """Initialize the database and create the users and bookings tables if they don't exist."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        
        # Create the users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT,  -- Add the email column
                join_date TEXT  -- Add the join_date column
            )
        ''')
        
        # Create the bookings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                departure_city TEXT NOT NULL,
                departure_airport TEXT NOT NULL,
                destination_city TEXT NOT NULL,
                destination_airport TEXT NOT NULL,
                departure_date TEXT NOT NULL,
                return_date TEXT,
                passengers INTEGER NOT NULL,
                total_price REAL NOT NULL,
                FOREIGN KEY (username) REFERENCES users(username)
            )
        ''')
        
        conn.commit()

def add_user(username, password):
    """Add a new user to the database."""
    password_hash = generate_password_hash(password)
    join_date = datetime.now().strftime('%Y-%m-%d')
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (username, password_hash, join_date)
                VALUES (?, ?, ?)
            ''', (username, password_hash, join_date))
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
        cursor.execute('SELECT username, email, join_date FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        if user:
            return {
                'username': user[0],
                'email': user[1],
                'join_date': user[2]
            }
        return None

def get_user_bookings(username):
    """Fetch booking history for a user."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, departure_city, departure_airport, destination_city, destination_airport,
                   departure_date, return_date, passengers, total_price
            FROM bookings
            WHERE username = ?
        ''', (username,))
        bookings = cursor.fetchall()
        return [
            {
                'id': booking[0],
                'departure_city': booking[1],
                'departure_airport': booking[2],
                'destination_city': booking[3],
                'destination_airport': booking[4],
                'departure_date': booking[5],
                'return_date': booking[6],
                'passengers': booking[7],
                'total_price': booking[8]
            }
            for booking in bookings
        ]