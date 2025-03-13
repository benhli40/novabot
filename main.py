import speech_recognition as sr
import time
import sys
from data_management.novabot_data_management import NovaBotDataManager
from modules.weather.weather import Weather
from modules.weather.weather_monitor import WeatherMonitor
from modules.entertainment.launch_game import GameScanner
from modules.entertainment.play_movie import MoviePlayer
from modules.entertainment.play_music import MusicPlayer
from modules.web_scraper import WebScraper

class NovaBot:
    def __init__(self):
        """Initialize LUMINA with all modules."""
        self.recognizer = sr.Recognizer()
        self.data_manager = NovaBotDataManager()
        self.weather = Weather()
        self.weather_monitor = WeatherMonitor()
        self.game_scanner = GameScanner([
            "C:\\Program Files\\",
            "C:\\Program Files (x86)\\",
            "E:\\Eve\\",
            "E:\\Program Files (x86)\\"
        ])
        self.movie_player = MoviePlayer()
        self.music_player = MusicPlayer()
        self.web_scraper = WebScraper()
        self.exit_commands = ["goodbye", "bye", "exit", "close"]
    
    def recognize_speech(self):
        """Listen for user input and process commands."""
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = self.recognizer.listen(source, timeout=8)
                command = self.recognizer.recognize_google(audio).lower()
                print(f"Recognized: {command}")
                
                if any(exit_word in command for exit_word in self.exit_commands):
                    print("Goodbye! Exiting LUMINA.")
                    sys.exit(0)
                
                self.process_command(command)
            except sr.UnknownValueError:
                print("Could not understand the command. Please try again.")
            except sr.RequestError:
                print("Could not request results from Google Speech Recognition service.")
            except sr.WaitTimeoutError:
                print("No speech detected. Please try again.")
    
    def process_command(self, command):
        """Process user commands and trigger the appropriate module."""
        if "weather" in command:
            location = command.replace("weather in", "").strip()
            print(f"Fetching weather for: {location}")
            print(self.weather.get_current_weather())
        elif "play" in command:
            if "on spotify" in command or "on pandora" in command:
                self.music_player.recognize_speech()
            elif "movie" in command or "watch" in command:
                self.movie_player.recognize_speech()
            elif "game" in command or "launch" in command:
                self.game_scanner.recognize_speech()
            else:
                print("Did you mean to play music, a movie, or launch a game?")
        elif "search" in command or "scrape" in command:
            print("What would you like me to find?")
            query = self.recognize_speech()
            if query:
                self.web_scraper.scrape(query)
        else:
            print("Command not recognized. Try again.")
    
    def run(self):
        """Continuously listen for user input until exit command is given."""
        print("LUMINA is now active. Say a command!")
        while True:
            self.recognize_speech()
            time.sleep(1)  # Prevent excessive looping

if __name__ == "__main__":
    novabot = NovaBot()
    novabot.run()