import os
import subprocess
import webbrowser
import speech_recognition as sr

class MoviePlayer:
    def __init__(self):
        """Initialize the MoviePlayer with supported platforms."""
        self.plex_base_url = "https://app.plex.tv/desktop/#!/search?query="
        self.emby_base_url = "http://localhost:8096/web/index.html#!/search?query="
        self.media_directory = "H:\\Media Overall"
        self.vlc_path = self.find_vlc()
        self.streaming_services = {
            "netflix": "https://www.netflix.com/search?q=",
            "paramount+": "https://www.paramountplus.com/shows/"
        }
        self.media_index = self.index_local_media()
    
    def find_vlc(self):
        """Find VLC media player executable path."""
        possible_paths = [
            "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe",
            "C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe"
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
        return None
    
    def index_local_media(self):
        """Index all movies and TV shows in the media directory."""
        media_files = {}
        for root, _, files in os.walk(self.media_directory):
            for file in files:
                if file.endswith((".mp4", ".mkv", ".avi", ".mov")):
                    title = os.path.splitext(file)[0].lower()
                    media_files[title] = os.path.join(root, file)
        print(f"Indexed {len(media_files)} media files.")
        return media_files
    
    def play_local_movie(self, platform, movie_name):
        """Launch Plex or Emby with a specified movie, or play directly if found in local media."""
        movie_name = movie_name.lower()
        if movie_name in self.media_index:
            print(f"Playing {movie_name} from local storage...")
            if self.vlc_path:
                subprocess.Popen([self.vlc_path, self.media_index[movie_name]])
            else:
                os.startfile(self.media_index[movie_name])  # Use default media player
        elif platform.lower() == "plex":
            print(f"Searching for {movie_name} in Plex...")
            webbrowser.open(self.plex_base_url + movie_name.replace(" ", "+"))
        elif platform.lower() == "emby":
            print(f"Searching for {movie_name} in Emby...")
            webbrowser.open(self.emby_base_url + movie_name.replace(" ", "+"))
        else:
            print(f"Error: {platform} is not a supported local media service.")
    
    def play_streaming_movie(self, service, movie_name):
        """Search and open a movie on Netflix or Paramount+."""
        service = service.lower()
        if service in self.streaming_services:
            search_url = self.streaming_services[service] + movie_name.replace(" ", "+")
            print(f"Opening {movie_name} on {service.capitalize()}...")
            webbrowser.open(search_url)
        else:
            print("Error: Streaming service not supported.")
    
    def recognize_speech(self):
        """Use voice commands to play a movie on a specified service."""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening for a movie request...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = recognizer.listen(source, timeout=8)
                command = recognizer.recognize_google(audio).lower()
                print(f"Recognized: {command}")
                
                if "on" in command and "play" in command:
                    before_on, after_on = command.split(" on ", 1)
                    if "play " in before_on:
                        movie_name = before_on.replace("play ", "").strip()
                    else:
                        movie_name = before_on.strip()
                    
                    words = after_on.split()
                    service = words[0]
                    
                    if service in self.streaming_services:
                        self.play_streaming_movie(service, movie_name)
                    elif service in ["plex", "emby"]:
                        self.play_local_movie(service, movie_name)
                    else:
                        print("Service not recognized. Try again.")
                else:
                    print(f"Command not recognized. Heard: '{command}'. Expected format: 'On <service> play <movie name>'.")
            except sr.UnknownValueError:
                print("Could not understand the command. Please try again.")
            except sr.RequestError:
                print("Could not request results from Google Speech Recognition service.")
            except sr.WaitTimeoutError:
                print("No speech detected. Please try again.")
    
# Example Usage
if __name__ == "__main__":
    player = MoviePlayer()
    
    # Example: Recognize speech for playing movies
    player.recognize_speech()