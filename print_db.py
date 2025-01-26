import sqlite3
import json

# Connect to the database
DATABASE = 'users.db'
conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

# Query the users table
cursor.execute('SELECT * FROM users')
users = cursor.fetchall()

# Print user data
print("Users Table:")
for user in users:
    # Handle cases where past_flights is NULL or missing
    if len(user) == 4:  # All columns are present
        user_id, username, password_hash, past_flights_json = user
    else:  # past_flights is missing (NULL)
        user_id, username, password_hash = user
        past_flights_json = None

    print(f"ID: {user_id}")
    print(f"Username: {username}")
    print(f"Password Hash: {password_hash}")

    # Deserialize past_flights JSON (if it exists)
    if past_flights_json:
        past_flights = json.loads(past_flights_json)
        print("Past Flights:")
        for flight in past_flights:
            print(f"  Flight Time: {flight['flight_time']} hours")
            print(f"  Price: ${flight['price']}")
            print(f"  Distance: {flight['distance']} miles")
    else:
        print("Past Flights: None")

    print("-" * 20)

# Query the airline_data table
cursor.execute('SELECT * FROM airline_data')
flights = cursor.fetchall()

# Print flight data
print("\nFlights Table:")
for flight in flights:
    flight_id, flight_time, price, distance = flight
    print(f"Flight ID: {flight_id}")
    print(f"Flight Time: {flight_time} hours")
    print(f"Price: ${price}")
    print(f"Distance: {distance} miles")
    print("-" * 20)

# Close the connection
conn.close()