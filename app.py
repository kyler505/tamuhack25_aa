from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Dummy flight data for demonstration
dummy_flights = [
    {
        "airline": "Spirit Airlines",
        "departure_time": "5:50 AM",
        "departure_airport": "IAH - Mar 1",
        "arrival_time": "10:58 AM",
        "arrival_airport": "LXX - Mar 8",
        "duration": "3h 08m",
        "price": "61.86"
    },
    {
        "airline": "Delta Airlines",
        "departure_time": "7:00 AM",
        "departure_airport": "IAH - Mar 1",
        "arrival_time": "12:00 PM",
        "arrival_airport": "LAX - Mar 8",
        "duration": "5h 00m",
        "price": "120.50"
    },
    {
        "airline": "American Airlines",
        "departure_time": "6:30 AM",
        "departure_airport": "IAH - Mar 1",
        "arrival_time": "11:30 AM",
        "arrival_airport": "LAX - Mar 8",
        "duration": "5h 00m",
        "price": "150.00"
    }
]

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

    # Get form data
    departure = request.form['departure']
    destination = request.form['destination']
    departure_date = request.form['departure_date']
    return_date = request.form['return_date']
    passengers = request.form['passengers']

    # For now, use dummy flight data
    results = dummy_flights

    return render_template('search_results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)