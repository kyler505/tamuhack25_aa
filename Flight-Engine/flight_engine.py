import requests

# efine the Flight Engine API endpoint

# TODO: please change this url
FLIGHT_ENGINE_URL = "http://localhost:3000/flights"

def fetch_flight_data():
    """Fetch flight data from the Flight Engine API."""
    response = requests.get(FLIGHT_ENGINE_URL)
    if response.status_code == 200:
        return response.json()  # parse JSON response
    else:
        print("Failed to fetch flights:", response.status_code)
        return []