import requests
import sqlite3
import schedule
import time
from datetime import datetime
import matplotlib.pyplot as plt

# OpenWeatherMap API key
API_KEY = 'your_api_key_here'  # Replace with your OpenWeatherMap API key
CITY_IDS = {'Delhi': 1273294, 'Mumbai': 1275339, 'Chennai': 1264527, 'Bangalore': 1277333, 'Kolkata': 1275004, 'Hyderabad': 1269843}

# Database setup for storing weather summaries
def setup_database():
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS weather_summary
                 (city TEXT, date TEXT, avg_temp REAL, max_temp REAL, min_temp REAL, dominant_condition TEXT)''')
    conn.commit()
    conn.close()

# Function to get weather data for a city
def get_weather_data(city_id):
    url = f'http://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={API_KEY}'
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        weather_data = {
            'city': data['name'],
            'temp': data['main']['temp'] - 273.15,  # Convert Kelvin to Celsius
            'feels_like': data['main']['feels_like'] - 273.15,
            'condition': data['weather'][0]['main'],
            'timestamp': data['dt']
        }
        return weather_data
    else:
        print(f"Failed to get data for city_id {city_id}: {response.status_code}")
        return None

# Function to calculate daily summary (for now simplified)
def calculate_daily_summary(city, weather_data_list):
    if not weather_data_list:
        return

    temps = [data['temp'] for data in weather_data_list]
    avg_temp = sum(temps) / len(temps)
    max_temp = max(temps)
    min_temp = min(temps)
    
    # Dominant weather condition is the one appearing most frequently
    conditions = [data['condition'] for data in weather_data_list]
    dominant_condition = max(set(conditions), key=conditions.count)

    # Store summary in database
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()
    c.execute('INSERT INTO weather_summary VALUES (?, ?, ?, ?, ?, ?)',
              (city, datetime.now().strftime("%Y-%m-%d"), avg_temp, max_temp, min_temp, dominant_condition))
    conn.commit()
    conn.close()

    return {
        'avg_temp': avg_temp,
        'max_temp': max_temp,
        'min_temp': min_temp,
        'dominant_condition': dominant_condition
    }

# Threshold alerting system
def check_threshold_alerts(city, weather_data, threshold_temp):
    if weather_data['temp'] > threshold_temp:
        print(f"Alert: Temperature in {city} has exceeded {threshold_temp}°C. Current temp: {weather_data['temp']}°C")

# Function to visualize data (simple plot for temperature trends)
def plot_weather_trends(city):
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()
    c.execute('SELECT date, avg_temp FROM weather_summary WHERE city = ?', (city,))
    data = c.fetchall()
    conn.close()

    if data:
        dates = [x[0] for x in data]
        temps = [x[1] for x in data]
        
        plt.plot(dates, temps, label=f'{city} Avg Temp')
        plt.xlabel('Date')
        plt.ylabel('Average Temperature (°C)')
        plt.title(f'Weather Trends for {city}')
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()

# Real-time weather monitoring
def monitor_weather(cities, threshold_temp=35):
    weather_data_collection = {city: [] for city in cities}

    for city, city_id in cities.items():
        weather_data = get_weather_data(city_id)
        if weather_data:
            weather_data_collection[city].append(weather_data)

            # Calculate and store daily summary
            calculate_daily_summary(city, weather_data_collection[city])

            # Check thresholds and trigger alerts
            check_threshold_alerts(city, weather_data, threshold_temp)

# Scheduled job to monitor weather every 5 minutes
def scheduled_weather_monitoring():
    monitor_weather(CITY_IDS)

# Initialize database
setup_database()

# Schedule the weather monitoring task to run every 5 minutes
schedule.every(5).minutes.do(scheduled_weather_monitoring)

# Run scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(1)
