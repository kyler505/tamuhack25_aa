from flask import Flask, render_template, request, redirect, url_for, session
from flask import Flask, render_template, request, redirect, url_for, session, flash
import database  # Import the database module
import requests  # For making HTTP requests to the Flight-Engine API
from datetime import datetime  # For parsing and formatting dates

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Initialize the database
database.init_db()

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
        password = request.form['password']

        if database.verify_user(username, password):
            session['username'] = username
            return redirect(url_for('flight_search'))
        else:
            flash('Invalid username or password', 'error')
            return render_template('login.html', username=username)
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if database.user_exists(username):
            flash('Username already exists', 'error')
        else:
            if database.add_user(username, password):
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Registration failed', 'error')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/flight_search')
def flight_search():
    if 'username' not in session:
        flash('You need to log in to access this page.', 'error')
        return redirect(url_for('login'))

    # Fetch past flights from the database
    past_flights = database.get_past_flights()
    return render_template('flight_search.html', past_flights=past_flights)

@app.route('/search', methods=['POST'])
def search():
    # Get form data from the search query
    trip_type = request.form.get('trip_type', 'Round-trip')  # Default to Round-trip
    departure = request.form.get('departure', '').upper()  # Convert to uppercase for IATA code
    destination = request.form.get('destination', '').upper()  # Convert to uppercase for IATA code
    departure_date = request.form.get('departure_date', '')
    return_date = request.form.get('return_date', '')  # Optional for one-way trips
    passengers = request.form.get('passengers', '1')  # Default to 1 Adult

    # Store the search details in the session
    session['last_search'] = {
        'trip_type': trip_type,
        'departure': departure,
        'destination': destination,
        'departure_date': departure_date,
        'return_date': return_date if trip_type == 'Round-trip' else None,  # Save return_date only for round-trips
        'passengers': passengers
    }

    # Get price range from the form (if provided)
    min_price = float(request.form.get('min_price', 0))
    max_price = float(request.form.get('max_price', float('inf')))

    # Fetch flights from the API (as before)
    try:
        outbound_response = requests.get(
            f'{FLIGHT_ENGINE_API_URL}/flights?date={departure_date}&origin={departure}&destination={destination}'
        )
        outbound_response.raise_for_status()
        outbound_flights = outbound_response.json()

        return_flights = []
        if trip_type == 'Round-trip' and return_date:
            return_response = requests.get(
                f'{FLIGHT_ENGINE_API_URL}/flights?date={return_date}&origin={destination}&destination={departure}'
            )
            return_response.raise_for_status()
            return_flights = return_response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error fetching flights: {e}")
        return render_template('search_results.html', results=[], error="Failed to fetch flight data. Please try again.")

    # Filter flights by price
    filtered_flights = []
    for outbound_flight in outbound_flights:
        outbound_price = outbound_flight.get("price", 0)
        if min_price <= outbound_price <= max_price:
            # Format outbound flight data
            outbound_departure_time = datetime.strptime(outbound_flight.get("departureTime"), "%Y-%m-%dT%H:%M:%S.%f%z")
            outbound_arrival_time = datetime.strptime(outbound_flight.get("arrivalTime"), "%Y-%m-%dT%H:%M:%S.%f%z")

            outbound_data = {
                "airline": "American Airlines",
                "departure_time": outbound_departure_time.strftime("%I:%M %p"),  # Format as "03:46 AM"
                "departure_date": outbound_departure_time.strftime("%b %d, %Y"),  # Format as "Jan 25, 2025"
                "departure_airport": outbound_flight.get("origin", {}).get("code", "N/A"),
                "departure_city": outbound_flight.get("origin", {}).get("city", "N/A"),
                "arrival_time": outbound_arrival_time.strftime("%I:%M %p"),  # Format as "04:20 AM"
                "arrival_date": outbound_arrival_time.strftime("%b %d, %Y"),  # Format as "Jan 25, 2025"
                "arrival_airport": outbound_flight.get("destination", {}).get("code", "N/A"),
                "arrival_city": outbound_flight.get("destination", {}).get("city", "N/A"),
                "duration": outbound_flight.get("duration", {}).get("locale", "N/A"),
                "price": outbound_flight.get("price", "N/A"),
                "aircraft": outbound_flight.get("aircraft", {}).get("model", "N/A"),
            }

            # For round-trip, pair outbound flight with a return flight
            if trip_type == 'Round-trip' and return_flights:
                for return_flight in return_flights:
                    return_price = return_flight.get("price", 0)
                    if min_price <= return_price <= max_price:
                        # Format return flight data (as before)
                        return_departure_time = datetime.strptime(return_flight.get("departureTime"), "%Y-%m-%dT%H:%M:%S.%f%z")
                        return_arrival_time = datetime.strptime(return_flight.get("arrivalTime"), "%Y-%m-%dT%H:%M:%S.%f%z")

                        return_data = {
                            "airline": "American Airlines",
                            "departure_time": return_departure_time.strftime("%I:%M %p"),  # Format as "03:46 AM"
                            "departure_date": return_departure_time.strftime("%b %d, %Y"),  # Format as "Jan 25, 2025"
                            "departure_airport": return_flight.get("origin", {}).get("code", "N/A"),
                            "departure_city": return_flight.get("origin", {}).get("city", "N/A"),
                            "arrival_time": return_arrival_time.strftime("%I:%M %p"),  # Format as "04:20 AM"
                            "arrival_date": return_arrival_time.strftime("%b %d, %Y"),  # Format as "Jan 25, 2025"
                            "arrival_airport": return_flight.get("destination", {}).get("code", "N/A"),
                            "arrival_city": return_flight.get("destination", {}).get("city", "N/A"),
                            "duration": return_flight.get("duration", {}).get("locale", "N/A"),
                            "price": return_price,
                            "aircraft": return_flight.get("aircraft", {}).get("model", "N/A"),
                        }

                        # Calculate combined price for round-trip
                        combined_price = f"{outbound_price + return_price:.2f}"

                        # Add to filtered flights
                        filtered_flights.append({
                            "outbound": outbound_data,
                            "return": return_data,
                            "combined_price": combined_price,
                        })
            else:
                # For one-way trips, only include outbound flights
                filtered_flights.append({
                    "outbound": outbound_data,
                    "return": None,
                    "combined_price": f"{outbound_price:.2f}",
                })

    # Render the search results template with the filtered flights
    return render_template('search_results.html', results=filtered_flights, trip_type=trip_type, departure=departure, destination=destination, departure_date=departure_date, return_date=return_date, passengers=passengers)

@app.route('/my_account')
def my_account():
    if 'username' not in session:
        flash('You need to log in to access this page.', 'error')
        return redirect(url_for('login'))

    username = session['username']
    user = database.get_user_details(username)
    return render_template('my_account.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)