"""
LUMINA SYSTEM ARCHITECTURE OVERVIEW
-----------------------------------
This high-level structure outlines how LUMINA's core components interact, including:
- Data Management (CRUD operations, retention policies)
- AI Processing (LLM-based responses, decision-making)
- Web Scraping (Dynamic content gathering)
- Weather Monitoring (Real-time alerts & user weather queries)

Each module will communicate via a central controller, ensuring LUMINA makes informed decisions based on stored and real-time data.
"""

import sys
import os

# Dynamically add the project root to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_management.lumina_data_management import LuminaDataManager
from modules.weather.weather_monitor import WeatherMonitor
from modules.weather.weather import Weather
from modules.web_scraper import WebScraper

class LuminaCore:
    def __init__(self):
        self.data_manager = LuminaDataManager()
        self.weather_monitor = WeatherMonitor()
        self.weather_checker = Weather()
        self.web_scraper = WebScraper()
        self.ai_processor = None  # Placeholder for LUMINA's LLM processing
    
        def handle_user_input(self, user_id, input_text, important=False):
            """Processes user input, handles weather queries, and stores conversations."""
            if "weather" in input_text.lower():
                return self.get_current_weather()
            if "search" in input_text.lower() or "scrape" in input_text.lower():
                return self.search_and_scrape(input_text)
            
            response = self.generate_response(input_text)
            self.data_manager.store_conversation(user_id, input_text, important)
            return response
    
    def generate_response(self, input_text):
        """Placeholder for AI processing - to be replaced with LUMINA's LLM."""
        return f"LUMINA: I acknowledge your message: {input_text}"
    
    def retrieve_important_conversations(self, user_id):
        """Fetches all important conversations for a given user."""
        return [convo for convo in self.data_manager.data_storage["conversations"] if convo["important"]]
    
    def delete_old_data(self):
        """Triggers LUMINA's cleanup process for non-essential data."""
        self.data_manager.delete_old_data()
    
    def get_current_weather(self):
        """Retrieves current weather conditions for the user."""
        return self.weather_checker.get_current_weather()
    
    def monitor_weather_conditions(self):
        """Checks for severe weather and takes action if necessary."""
        status = self.weather_monitor.check_severe_weather()
        if status == "shutdown":
            print("LUMINA: Severe weather detected. Shutting down to protect system.")
            exit()
    
    def search_and_scrape(self, query):
        """LUMINA searches the web for relevant information."""
        self.web_scraper.query = query.replace("search", "").replace("scrape", "").strip()
        self.web_scraper.scrape_and_store()
        return "LUMINA: I've gathered some relevant information."
    
    def save_system_state(self):
        """Saves all critical data before shutdown."""
        self.data_manager.save_to_file()
    
    def load_system_state(self):
        """Loads previous session data on startup."""
        self.data_manager.load_from_file()

# Example Usage
if __name__ == "__main__":
    lumina = LuminaCore()
    lumina.load_system_state()
    lumina.monitor_weather_conditions()  # Automatically check weather on startup
    print(lumina.handle_user_input("user1", "Search Python programming best practices"))
    lumina.delete_old_data()
    print("Important Conversations:", lumina.retrieve_important_conversations("user1"))
    lumina.save_system_state()