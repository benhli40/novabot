import os
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from the weather folder
dotenv_path = Path(__file__).parent / "weather" / ".env"
load_dotenv(dotenv_path)

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
USER_LOCATION = os.getenv("USER_LOCATION", "Marble Falls")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

class Weather:
    def __init__(self, location=USER_LOCATION):
        """Initialize with location."""
        self.location = location
    
    def get_current_weather(self):
        """Fetch current weather conditions from OpenWeather API."""
        params = {
            "q": self.location,
            "appid": OPENWEATHER_API_KEY,
            "units": "imperial"  # Change to "imperial" for Fahrenheit
        }
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            return self.format_weather(data)
        else:
            return "Error: Unable to retrieve weather data."
    
    def format_weather(self, data):
        """Formats weather data for user-friendly display."""
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        description = data["weather"][0]["description"].capitalize()
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        return (f"🌤 Weather in {self.location}:\n"
                f"🌡 Temperature: {temperature}°F (Feels like {feels_like}°F)\n"
                f"💨 Wind Speed: {wind_speed} m/h\n"
                f"💧 Humidity: {humidity}%\n"
                f"🌍 Condition: {description}")

# Example Usage
if __name__ == "__main__":
    weather = Weather()
    print(weather.get_current_weather())