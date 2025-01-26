import json
import os
from database import init_db, add_user, add_aa_flight, clear_airline_data



def main():
    # initialize the database
    init_db()
    clear_airline_data()

    
    # gets data from the generated flights, and adds it to the database into the aa_flights table
    
        
    # example data for users
    users = [
        {
            "username": "john_doe",
            "password": "password123",
            "past_flights": [
                {"flight_time": 2.5, "price": 347.28, "distance": 500.0},
                {"flight_time": 3.0, "price": 368.19, "distance": 600.0}
            ]
        },
        {
            "username": "jane_doe",
            "password": "password456",
            "past_flights": [
                {"flight_time": 4.0, "price": 602.11, "distance": 800.0},
                {"flight_time": 5.0, "price": 755.19, "distance": 1000.0}
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
            flight_time = flight["duration"]["hours"] + flight["duration"]["minutes"] / 60
    
            # Add the flight to the database
            add_aa_flight(
                flight_time=flight_time,
                price=flight["price"],
                distance=flight["distance"]
            )


    # add example users into the database
    for user in users:
        add_user(
            username=user["username"],
            password=user["password"],
            past_flights=user["past_flights"]
    )

if __name__ == "__main__":
    main()