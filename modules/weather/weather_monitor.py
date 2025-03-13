import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
USER_LOCATION = os.getenv("USER_LOCATION", "Marble Falls")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

SEVERE_WEATHER_CONDITIONS = {
    "thunderstorm": "⚠️ Severe Thunderstorm Alert! Potential risk of power surges.",
    "hail": "⚠️ Hail Warning! Protect your equipment.",
    "tornado": "🌪️ Tornado Warning! Immediate precautions advised.",
    "hurricane": "🌀 Hurricane Alert! High winds and heavy rain expected.",
    "extreme heat": "🔥 Extreme Heat Warning! Potential overheating risk.",
    "snowstorm": "❄️ Heavy Snowstorm Alert! Possible disruptions expected.",
    "high wind": "💨 High Wind Warning! Secure your devices and stay safe.",
    "flood": "🌊 Flood Warning! Ensure all equipment is safe from water damage."
}

class WeatherMonitor:
    def __init__(self, location=USER_LOCATION, alert_level="severe"):
        """Initialize with location and alert level ('all' or 'severe')."""
        self.location = location
        self.alert_level = alert_level  # 'severe' for only major alerts, 'all' for all weather events
    
    def get_weather_data(self):
        """Fetch current weather data from OpenWeather API."""
        params = {
            "q": self.location,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"  # Change to "imperial" for Fahrenheit
        }
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error: Unable to retrieve weather data.")
            return None
    
    def check_severe_weather(self):
        """Checks for severe weather conditions and returns alerts."""
        data = self.get_weather_data()
        if not data:
            return "Error fetching weather data."
        
        weather_conditions = [weather["main"].lower() for weather in data["weather"]]
        alerts = []
        shutdown_required = False
        
        for condition in weather_conditions:
            if condition in SEVERE_WEATHER_CONDITIONS:
                alerts.append(SEVERE_WEATHER_CONDITIONS[condition])
                if condition in ["thunderstorm", "hail", "tornado", "hurricane"]:
                    shutdown_required = True  # These require an emergency shutdown
        
        if alerts:
            for alert in alerts:
                print(alert)
            return "shutdown" if shutdown_required else "alert"
        
        print("✅ No severe weather detected.")
        return "safe"
    
# Example Usage
if __name__ == "__main__":
    weather_monitor = WeatherMonitor(alert_level="severe")  # Defaults to USER_LOCATION
    status = weather_monitor.check_severe_weather()
    if status == "shutdown":
        print("LUMINA should notify the user and exit safely.")