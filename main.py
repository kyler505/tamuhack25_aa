import json
import os
from database import init_db, add_user, clear_airline_data, add_aa_flight
import random

def generate_past_flights(trend, num_flights=5):
    flights = []
    for _ in range(num_flights):
        if trend == "short_flight_time":
            flight_time = round(random.uniform(1.0, 3.0), 2)  # Short flight times (1-3 hours)
            price = round(random.uniform(200.0, 400.0), 2)    # Moderate price
            distance = round(random.uniform(300.0, 600.0), 2) # Moderate distance
        elif trend == "low_price":
            flight_time = round(random.uniform(2.0, 6.0), 2)  # Moderate flight times
            price = round(random.uniform(100.0, 300.0), 2)    # Low price
            distance = round(random.uniform(200.0, 500.0), 2) # Short to moderate distance
        elif trend == "long_distance":
            flight_time = round(random.uniform(4.0, 8.0), 2)  # Long flight times
            price = round(random.uniform(500.0, 1000.0), 2)   # High price
            distance = round(random.uniform(1000.0, 2000.0), 2) # Long distance
        else:
            flight_time = round(random.uniform(1.0, 8.0), 2)  # Random flight times
            price = round(random.uniform(100.0, 1000.0), 2)   # Random price
            distance = round(random.uniform(200.0, 2000.0), 2) # Random distance

        flights.append({
            "flight_time": flight_time,
            "price": price,
            "distance": distance
        })
    return flights

def main():
    # initialize the database
    init_db()
    clear_airline_data()
    
    # Function to generate past flights based on trends

    # Define the users and their trends
    users = [
        {
            "username": "john_doe",
            "password": "password123",
            "past_flights": generate_past_flights("short_flight_time")  # Prefers short flight times
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
   
        
        
        
    # example data for users
    # users = [
    #     {
    #         "username": "john_doe",
    #         "password": "password123",
    #         "past_flights": [
    #             {"flight_time": 2.53, "price": 347.28, "distance": 500.0},
    #             {"flight_time": 3.01, "price": 368.19, "distance": 600.0}
    #         ]
    #     },
    #     {
    #         "username": "jane_doe",
    #         "password": "password456",
    #         "past_flights": [
    #             {"flight_time": 4.05, "price": 602.11, "distance": 800.0},
    #             {"flight_time": 5.04, "price": 755.19, "distance": 1000.0}
    #         ]
    #     }
    # ]

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