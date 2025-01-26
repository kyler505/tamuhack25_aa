from flask import Flask, render_template, request, redirect, url_for, session
import requests  # For making HTTP requests to the Flight-Engine API
from datetime import datetime  # For parsing and formatting dates

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Flight-Engine API base URL
FLIGHT_ENGINE_API_URL = 'http://localhost:4000'  # Update if the API is hosted elsewhere

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('flight_search'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect(url_for('flight_search'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/flight_search')
def flight_search():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('flight_search.html')

@app.route('/search', methods=['POST'])
def search():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Get form data from the search query
    trip_type = request.form.get('trip_type', 'Round-trip')  # Default to Round-trip
    departure = request.form.get('departure', '').upper()  # Convert to uppercase for IATA code
    destination = request.form.get('destination', '').upper()  # Convert to uppercase for IATA code
    departure_date = request.form.get('departure_date', '')
    return_date = request.form.get('return_date', '')  # Optional for one-way trips
    passengers = request.form.get('passengers', '1')  # Default to 1 Adult

    # Validate required fields
    if not departure or not destination or not departure_date:
        return render_template('search_results.html', results=[], error="Please fill in all required fields.")

    try:
        # Fetch outbound flights
        outbound_response = requests.get(
            f'{FLIGHT_ENGINE_API_URL}/flights?date={departure_date}&origin={departure}&destination={destination}'
        )
        outbound_response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        outbound_flights = outbound_response.json()

        # Fetch return flights for round-trip
        return_flights = []
        if trip_type == 'Round-trip' and return_date:
            return_response = requests.get(
                f'{FLIGHT_ENGINE_API_URL}/flights?date={return_date}&origin={destination}&destination={departure}'
            )
            return_response.raise_for_status()
            return_flights = return_response.json()

    except requests.exceptions.RequestException as e:
        # Handle API errors gracefully
        print(f"Error fetching flights: {e}")
        return render_template('search_results.html', results=[], error="Failed to fetch flight data. Please try again.")

    # Map flight data to the structure expected by the template
    filtered_flights = []
    for outbound_flight in outbound_flights:
        # Format outbound flight data
        outbound_departure_time = datetime.strptime(outbound_flight.get("departureTime"), "%Y-%m-%dT%H:%M:%S.%f%z")
        outbound_arrival_time = datetime.strptime(outbound_flight.get("arrivalTime"), "%Y-%m-%dT%H:%M:%S.%f%z")

        outbound_data = {
            "airline": "Unknown Airline",  # Replace with actual airline data if available
            "departure_time": outbound_departure_time.strftime("%I:%M %p"),  # Format as "02:36 AM"
            "departure_date": outbound_departure_time.strftime("%b %d, %Y"),  # Format as "Jan 26, 2025"
            "departure_airport": outbound_flight.get("origin", {}).get("code", "N/A"),
            "departure_city": outbound_flight.get("origin", {}).get("city", "N/A"),
            "arrival_time": outbound_arrival_time.strftime("%I:%M %p"),  # Format as "05:11 AM"
            "arrival_date": outbound_arrival_time.strftime("%b %d, %Y"),  # Format as "Jan 26, 2025"
            "arrival_airport": outbound_flight.get("destination", {}).get("code", "N/A"),
            "arrival_city": outbound_flight.get("destination", {}).get("city", "N/A"),
            "duration": outbound_flight.get("duration", {}).get("locale", "N/A"),
            "price": "N/A"  # Replace with actual price data if available
        }

        # For round-trip, pair outbound flight with a return flight
        if trip_type == 'Round-trip' and return_flights:
            for return_flight in return_flights:
                # Format return flight data
                return_departure_time = datetime.strptime(return_flight.get("departureTime"), "%Y-%m-%dT%H:%M:%S.%f%z")
                return_arrival_time = datetime.strptime(return_flight.get("arrivalTime"), "%Y-%m-%dT%H:%M:%S.%f%z")

                return_data = {
                    "airline": "Unknown Airline",  # Replace with actual airline data if available
                    "departure_time": return_departure_time.strftime("%I:%M %p"),  # Format as "02:36 AM"
                    "departure_date": return_departure_time.strftime("%b %d, %Y"),  # Format as "Jan 26, 2025"
                    "departure_airport": return_flight.get("origin", {}).get("code", "N/A"),
                    "departure_city": return_flight.get("origin", {}).get("city", "N/A"),
                    "arrival_time": return_arrival_time.strftime("%I:%M %p"),  # Format as "05:11 AM"
                    "arrival_date": return_arrival_time.strftime("%b %d, %Y"),  # Format as "Jan 26, 2025"
                    "arrival_airport": return_flight.get("destination", {}).get("code", "N/A"),
                    "arrival_city": return_flight.get("destination", {}).get("city", "N/A"),
                    "duration": return_flight.get("duration", {}).get("locale", "N/A"),
                    "price": "N/A"  # Replace with actual price data if available
                }

                # Pair outbound and return flights
                filtered_flights.append({
                    "outbound": outbound_data,
                    "return": return_data
                })
        else:
            # For one-way trips, only include outbound flights
            filtered_flights.append({
                "outbound": outbound_data,
                "return": None  # No return flight for one-way trips
            })

    # Render the search results template with the filtered flights and search parameters
    return render_template('search_results.html', results=filtered_flights, trip_type=trip_type, departure=departure, destination=destination, departure_date=departure_date, return_date=return_date, passengers=passengers)

if __name__ == '__main__':
    app.run(debug=True)