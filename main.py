from database import init_db, add_aa_flight, add_user
from flight_engine import fetch_flight_data

def main():
    # initialize the database
    init_db()

    # fetch flight data from the Flight Engine API
    aa_flights = fetch_flight_data()

    # insert fetched flight data into the database
    # TODO: add key-value pairs also in database.py
    for flight in aa_flights:
        add_aa_flight(
            flight["flight_time"],
            flight["price"],
            flight["distance"]
        )
        
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
                {"flight_time": 4.0, "price": 250.0, "distance": 800.0},
                {"flight_time": 5.0, "price": 300.0, "distance": 1000.0}
            ]
        }
    ]

    # add example users into the database
    for user in users:
        add_user(
            username=user["username"],
            password=user["password"],
            past_flights=user["past_flights"]
    )

if __name__ == "__main__":
    main()