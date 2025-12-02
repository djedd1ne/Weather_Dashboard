import requests
import os
from dotenv import load_dotenv

#Load .env
load_dotenv()
API_KEY = os.environ.get("API_KEY")
if API_KEY:
    print ("API key loaded successfully.")
else:
    print("Error: API_KEY not found.")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def fetch_weather(city):
    params = {
        "q" : city,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(BASE_URL, params=params)
    #https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API_key}&units=metrics
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
#Example

city = "London"
weather_data = fetch_weather(city)
if weather_data:
    print(weather_data)
