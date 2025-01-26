import json
import os
from database import init_db, add_user, clear_airline_data, add_aa_flight



def main():
    # initialize the database
    init_db()
    clear_airline_data()
    
        
    # example data for users
    users = [
        {
            "username": "john_doe",
            "password": "password123",
            "past_flights": [
                {"flight_time": 2.53, "price": 347.28, "distance": 500.0},
                {"flight_time": 3.01, "price": 368.19, "distance": 600.0}
            ]
        },
        {
            "username": "jane_doe",
            "password": "password456",
            "past_flights": [
                {"flight_time": 4.05, "price": 602.11, "distance": 800.0},
                {"flight_time": 5.04, "price": 755.19, "distance": 1000.0}
            ]
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

if __name__ == "__main__":
    main()