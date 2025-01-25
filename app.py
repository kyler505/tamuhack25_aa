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
        # Fetch flight data from the Flight-Engine API using the departure date, origin, and destination
        response = requests.get(
            f'{FLIGHT_ENGINE_API_URL}/flights?date={departure_date}&origin={departure}&destination={destination}'
        )
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        flights = response.json()
    except requests.exceptions.RequestException as e:
        # Handle API errors gracefully
        print(f"Error fetching flights: {e}")
        return render_template('search_results.html', results=[], error="Failed to fetch flight data. Please try again.")

    # Map flight data to the structure expected by the template
    filtered_flights = []
    for flight in flights:
        departure_time = datetime.strptime(flight.get("departureTime"), "%Y-%m-%dT%H:%M:%S.%f%z")
        arrival_time = datetime.strptime(flight.get("arrivalTime"), "%Y-%m-%dT%H:%M:%S.%f%z")

        filtered_flights.append({
            "airline": "Unknown Airline",  # Replace with actual airline data if available
            "departure_time": departure_time.strftime("%I:%M %p"),  # Format as "02:36 AM"
            "departure_date": departure_time.strftime("%b %d, %Y"),  # Format as "Jan 26, 2025"
            "departure_airport": flight.get("origin", {}).get("code", "N/A"),
            "departure_city": flight.get("origin", {}).get("city", "N/A"),
            "arrival_time": arrival_time.strftime("%I:%M %p"),  # Format as "05:11 AM"
            "arrival_date": arrival_time.strftime("%b %d, %Y"),  # Format as "Jan 26, 2025"
            "arrival_airport": flight.get("destination", {}).get("code", "N/A"),
            "arrival_city": flight.get("destination", {}).get("city", "N/A"),
            "duration": flight.get("duration", {}).get("locale", "N/A"),
            "price": "N/A"  # Replace with actual price data if available
        })

    # Render the search results template with the filtered flights
    return render_template('search_results.html', results=filtered_flights)

if __name__ == '__main__':
    app.run(debug=True)