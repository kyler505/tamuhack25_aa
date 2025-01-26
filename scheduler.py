# for a practical use, where users' data will constantly be updated


# import time
# import schedule
# from database import init_db, add_flight
# from flight_engine import fetch_flight_data

# def update_flights():
#     """Fetch flight data and update the database."""
#     flights = fetch_flight_data()
#     for flight in flights:
#         add_flight(
#             flight["flight_number"],
#             flight["origin"],
#             flight["destination"],
#             flight["departure_time"],
#             flight["arrival_time"],
#             flight["price"],
#             flight["distance"]
#         )
#     print("Flight data updated at:", time.ctime())

# # schedule the update_flights function to run every hour
# schedule.every().hour.do(update_flights)

# # Keep the script running
# if __name__ == "__main__":
#     init_db()
#     while True:
#         schedule.run_pending()
#         time.sleep(1)