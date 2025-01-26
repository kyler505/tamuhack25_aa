import json
import os
from database import init_db, add_user, clear_airline_data, add_aa_flight

from training import generate_past_flights, cluster
from flask import session

def main():
    # initialize the database
    init_db()
    clear_airline_data()
    # delete_all_users()
    
    # Function to generate past flights based on trends

    # Define the users and their trends
    users = [
        {
            "username": "john_doe",
            "password": "password123",
            "past_flights": generate_past_flights("early_flight_time")  # Prefers early flight times
        },
        {
            "username": "jane_doe",
            "password": "password456",
            "past_flights": generate_past_flights("low_price")  # Prefers low prices
        },
        {
            "username": "alice_smith",
            "password": "password789",
            "past_flights": generate_past_flights("long_distance")  # Prefers long distances
        },
        {
            "username": "bob_jones",
            "password": "password101",
            "past_flights": generate_past_flights("random")  # No specific trend
        }
    ]

    # Get the directory of the current script
    script_dir = os.path.dirname(__file__)
    
    # Construct the path to the JSON file
    json_file_path = os.path.join(script_dir, 'Flight-Engine\\generatedFlights.json')
    
    # Load JSON data from file
    with open(json_file_path, 'r') as file:
        aa_flights = json.load(file)
        for flight in aa_flights:
            # Calculate flight_time in hours
            flight_time = round(flight["duration"]["hours"] + flight["duration"]["minutes"] / 60, 2)
    
            # Add the flight to the database
            add_aa_flight(
                flight_time=flight_time,
                price=flight["price"],
                distance=flight["distance"]
            )

    # # add example users into the database
    for user in users:
        add_user(
            username=user["username"],
            password=user["password"],
            past_flights=user["past_flights"]
    )

# Iterate through users and check if the username matches the session
    # for user in users:
    #     if user["username"] == session.get("username"):
    #         current_user = user
    #         break  # Exit the loop once the user is found
    cluster("john_doe")
    # cluster(current_user["username"])

if __name__ == "__main__":
    main()