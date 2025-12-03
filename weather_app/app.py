from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

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

def parse_weather(data):
    return {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"]
    }

@app.route('/', methods=["GET", "POST"])
def home():
    weather = None
    if request.method == "POST":
        city = request.form.get("city")
        data = fetch_weather(city)
        if data:
            weather = parse_weather(data)
    return render_template("index.html", weather=weather)

if __name__ == "__main__":
    app.run(debug= True)