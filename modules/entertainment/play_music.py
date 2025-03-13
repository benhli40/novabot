import os
import subprocess
import webbrowser
import speech_recognition as sr

class MusicPlayer:
    def __init__(self):
        """Initialize the MusicPlayer with supported platforms."""
        self.spotify_path = "C:\\Users\\Admin\\AppData\\Roaming\\Spotify\\Spotify.exe"
        self.pandora_url = "https://www.pandora.com/search/"
        self.spotify_web_url = "https://open.spotify.com/search/"
    
    def play_spotify(self, song_or_artist):
        """Play a song or artist in the Spotify desktop app or web."""
        if os.path.exists(self.spotify_path):
            print(f"Opening Spotify app for {song_or_artist}...")
            subprocess.Popen([self.spotify_path])
        else:
            print(f"Searching for {song_or_artist} on Spotify Web...")
            search_url = self.spotify_web_url + song_or_artist.replace(" ", "%20")
            webbrowser.open(search_url)
    
    def play_pandora(self, song_or_artist):
        """Search and play a song or artist on Pandora."""
        print(f"Searching for {song_or_artist} on Pandora...")
        search_url = self.pandora_url + song_or_artist.replace(" ", "%20")
        webbrowser.open(search_url)
    
    def recognize_speech(self):
        """Use voice commands to play music on a specified platform."""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening for a music request...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = recognizer.listen(source, timeout=8)
                command = recognizer.recognize_google(audio).lower()
                print(f"Recognized: {command}")
                
                words = command.split()
                if "on" in words and "play" in words:
                    play_index = words.index("play")
                    on_index = words.index("on")
                    
                    if play_index < on_index:
                        song_or_artist = " ".join(words[play_index + 1:on_index])
                        service = words[on_index + 1]
                        
                        if service == "spotify":
                            self.play_spotify(song_or_artist)
                        elif service == "pandora":
                            self.play_pandora(song_or_artist)
                        else:
                            print("Service not recognized. Try 'On Spotify play' or 'On Pandora play'.")
                    else:
                        print("Invalid command format. Try 'On <service> play <song or artist>'.")
                else:
                    print(f"Command not recognized. Heard: '{command}'. Expected format: 'On <service> play <song or artist>'.")
            except sr.UnknownValueError:
                print("Could not understand the command. Please try again.")
            except sr.RequestError:
                print("Could not request results from Google Speech Recognition service.")
            except sr.WaitTimeoutError:
                print("No speech detected. Please try again.")
    
# Example Usage
if __name__ == "__main__":
    player = MusicPlayer()
    
    # Example: Recognize speech for playing music
    player.recognize_speech()