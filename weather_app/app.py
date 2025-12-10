from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load .env
load_dotenv()
API_KEY = os.environ.get("API_KEY")
if API_KEY:
    print("API key loaded successfully.")
else:
    print("Error: API_KEY not found.")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def fetch_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(BASE_URL, params=params)
    
    # http request failed
    if response.status_code != 200:
        return {"success": False, "error": response.json().get("message")}
    
    # http request succeeded check cod
    data = response.json()
    cod = str(data.get("cod"))
    
    if cod == "200":
        return {"success": True, "data": data}
    else:
        return {"success": False, "error": data.get("message")}


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
    error = None

    if request.method == "POST":
        city = request.form.get("city")
        result = fetch_weather(city)
        if result["success"]:
            weather = parse_weather(result["data"])
        else:
            error = result["error"]
    return render_template("index.html", weather=weather, error=error)


if __name__ == "__main__":
    app.run(debug=True)