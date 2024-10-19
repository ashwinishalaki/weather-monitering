import requests
import schedule
import time
from datetime import datetime, date
from database import get_session
from models import DailySummary, Alert
from sqlalchemy.exc import SQLAlchemyError

# Constants
API_KEY = '6c5f665ff170d2e923f1284bc5ea2f75' #our_openweathermap_api_key
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
API_URL = "https://home.openweathermap.org/api_keys"
API_LINK = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}"
TEMP_THRESHOLD = 35.0  # Celsius

# Convert temp from Kelvin to Celsius
def kelvin_to_celsius(temp_kelvin):
    return temp_kelvin - 273.15

# Fetch weather data from OpenWeatherMap API
def fetch_weather_data(city):
    try:
        response = requests.get(API_URL.format(city, API_KEY), timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data for {city}: {e}")
        return None

# Process the weather data and return necessary fields
def process_weather_data(data, city):
    try:
        main_condition = data['weather'][0]['main']
        temp = kelvin_to_celsius(data['main']['temp'])
        timestamp = datetime.utcfromtimestamp(data['dt'])
        print(f"{city} - {timestamp} - Weather: {main_condition}, Temp: {temp:.2f}°C")
        return {'city': city, 'temp': temp, 'main_condition': main_condition, 'timestamp': timestamp}
    except (KeyError, TypeError) as e:
        print(f"Error processing data for {city}: {e}")
        return None

# Store into the database
def store_daily_summary(session, weather_data):
    try:
        today = date.today()
        city = weather_data['city']
        temp = weather_data['temp']
        condition = weather_data['main_condition']

        # Check if summary already exists for today
        summary = session.query(DailySummary).filter_by(city=city, date=today).first()
        if not summary:
            # New summary
            summary = DailySummary(
                city=city, date=today, avg_temp=temp, max_temp=temp, min_temp=temp, dominant_condition=condition
            )
            session.add(summary)
        else:
            # Update existing summary
            summary.avg_temp = (summary.avg_temp + temp) / 2  # Simplistic average
            summary.max_temp = max(summary.max_temp, temp)
            summary.min_temp = min(summary.min_temp, temp)
            summary.dominant_condition = condition
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error saving summary for {city}: {e}")

# Log temperature alerts into the database
def log_alert(session, city, condition):
    try:
        alert = Alert(city=city, timestamp=datetime.now(), condition=condition)
        session.add(alert)
        session.commit()
        print(f"Alert logged for {city}: {condition}")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error logging alert for {city}: {e}")

# Check if temperature exceeds threshold and log alert
def check_alerts(session, weather_data):
    temp = weather_data['temp']
    city = weather_data['city']
    if temp > TEMP_THRESHOLD:
        condition = f"Temperature exceeds {TEMP_THRESHOLD}°C (Current: {temp:.2f}°C)"
        log_alert(session, city, condition)

# Fetch and process weather data for each city
def fetch_and_process():
    session_generator = get_session()
    session = next(session_generator)
    for city in CITIES:
        data = fetch_weather_data(city)
        if data:
            weather_data = process_weather_data(data, city)
            if weather_data:
                store_daily_summary(session, weather_data)
                check_alerts(session, weather_data)
    session_generator.close()

# Schedule tasks to run at specific intervals
schedule.every(5).minutes.do(fetch_and_process)

# Main loop to run scheduled tasks
if __name__ == "_main_":
    print("Weather Monitoring System Started.")
    while True:
        schedule.run_pending()
        time.sleep(1)