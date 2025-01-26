# FlightPath ✈️
FlightPath is a personalized flight optimization platform designed to enhance the passenger experience for American Airlines. By analyzing user preferences, flight history, and real-time data, FlightPath recommends tailored flight options that align with individual needs—whether it's sightseeing, activities, or cost efficiency.

TAMUHACK 2025 Challenge - Kyler Cao, Brady Nguyen, Erix Huynh, Kevin Nguyen

# Setup:
Step 1: Clone the Repository
git clone https://github.com/kyler505/tamuhack25_aa


Run the following commands on a bash terminal:
Step 2: Set Up a Virtual Environment

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Step 3: Install Dependencies
pip install -r requirements.txt


Step 4: Intialize the Database
python -c "from database import init_db; init_db()"

Step 5: Run the Application
export FLASK_APP=app.py  # On Windows: set FLASK_APP=app.py
flask run