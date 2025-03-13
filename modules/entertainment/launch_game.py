import os
import json
import winreg
import subprocess
import speech_recognition as sr
from difflib import get_close_matches

class GameScanner:
    def __init__(self, game_paths):
        """Initialize the game scanner with directories to scan."""
        self.game_paths = game_paths
        self.games = {}
        self.games_db = "game_list.json"  # Store detected games
        self.play_history = "play_history.json"  # Track game launches
        self.ignored_executables = ["uninstall.exe", "setup.exe", "launcher.exe"]  # Ignore common launchers
        self.launcher_associations = {
            "diablo iii": "Battle.net.exe",
            "diablo iv": "Battle.net.exe",
            "world of warcraft": "Battle.net.exe",
            "call of duty": "Battle.net.exe",
            "diablo immortal": "Battle.net.exe",
            "starcraft ii": "Battle.net.exe",
            "heroes of the storm": "Battle.net.exe",
            "overwatch 2": "Battle.net.exe",
            "hearthstone": "Battle.net.exe",
            "world of warcraft classic": "Battle.net.exe",
            "cyberpunk 2077": "GOG Galaxy.exe",
            "elden ring": "Steam.exe",
            "adventure capitalist": "Steam.exe",
            "caesar iii": "Steam.exe",
            "counter-strike 2": "Steam.exe",
            "the elder scrolls": "Steam.exe",
            "fallout shelter": "Steam.exe",
            "mobius final fantasy": "Steam.exe",
            "pharaoh": "Steam.exe",
            "rica": "Steam.exe",
            "risk": "Styeam.exe",
            "skyforge": "Steam.exe",
            "stronghold crusader extreme hd": "Steam.exe",
            "stronghold crusader hd": "Steam.exe",
            "stronghold hd": "Steam.exe",
            "vindictus": "Steam.exe",
            "warframe": "Steam.exe",
            "white pearl": "Steam.exe",
            "zeus": "Steam.exe"
        }
    
    def scan_for_games(self):
        """Scan the specified directories for installed games."""
        print("Scanning for installed games...")
        
        # Scan directories for game executables
        for path in self.game_paths:
            if os.path.exists(path):
                for root, dirs, files in os.walk(path):
                    exe_files = [file for file in files if file.endswith(".exe") and file.lower() not in self.ignored_executables]
                    
                    if exe_files:
                        # Prioritize game executables over launchers
                        main_exe = self.select_best_executable(root, exe_files)
                        game_name = main_exe.replace(".exe", "").lower()
                        self.games[game_name] = os.path.join(root, main_exe)
        
        # Scan Windows Registry for installed games
        self.scan_registry()
        
        self.save_games()
        print(f"Detected {len(self.games)} games.")
    
    def select_best_executable(self, root, exe_files):
        """Select the best game executable by avoiding launchers and prioritizing main game files."""
        prioritized_files = [exe for exe in exe_files if "game" in exe.lower() or "diablo iii.exe" in exe.lower()]
        return prioritized_files[0] if prioritized_files else exe_files[0]
    
    def scan_registry(self):
        """Scan Windows Registry for installed games from known launchers."""
        print("Scanning Windows Registry for installed games...")
        registry_paths = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ]
        
        for reg_path in registry_paths:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
                    for i in range(0, winreg.QueryInfoKey(key)[0]):
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            try:
                                game_name = winreg.QueryValueEx(subkey, "DisplayName")[0].lower()
                                install_location = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                                if install_location and os.path.exists(install_location):
                                    for file in os.listdir(install_location):
                                        if file.endswith(".exe") and file.lower() not in self.ignored_executables:
                                            self.games[game_name] = os.path.join(install_location, file)
                            except FileNotFoundError:
                                continue
            except FileNotFoundError:
                continue
    
    def save_games(self):
        """Save detected games to a JSON file for later use."""
        with open(self.games_db, "w") as f:
            json.dump(self.games, f, indent=4)
    
    def load_games(self):
        """Load previously detected games from the JSON file."""
        if os.path.exists(self.games_db):
            with open(self.games_db, "r") as f:
                self.games = json.load(f)
        return self.games
    
    def track_play_history(self, game_name):
        """Track how often a game is played to improve suggestions."""
        history = {}
        if os.path.exists(self.play_history):
            with open(self.play_history, "r") as f:
                history = json.load(f)
        
        history[game_name] = history.get(game_name, 0) + 1
        with open(self.play_history, "w") as f:
            json.dump(history, f, indent=4)
        
        print(f"Updated play count for {game_name}.")
    
    def launch_game(self, game_name):
        """Launch a game, allowing fuzzy matching for game names."""
        self.load_games()
        game_name = game_name.lower()
        
        # Attempt to find the closest match for the spoken game name
        matched_game = get_close_matches(game_name, self.games.keys(), n=1, cutoff=0.6)
        if matched_game:
            matched_game = matched_game[0]
            game_path = self.games[matched_game]
            print(f"Launching {matched_game.capitalize()}...")
            try:
                subprocess.Popen(game_path, shell=True)
                self.track_play_history(matched_game)
            except Exception as e:
                print(f"Error launching {matched_game}: {e}")
        else:
            print(f"Game '{game_name}' not found. Try scanning for games first.")
    
    def recognize_speech(self):
        """Use voice commands to launch a game."""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening for a game to launch...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = recognizer.listen(source, timeout=8)
                command = recognizer.recognize_google(audio).lower()
                print(f"Recognized: {command}")
                
                # Extract game name dynamically
                words = command.split()
                if "launch" in words:
                    game_name = " ".join(words[1:])  # Everything after "launch"
                    self.launch_game(game_name)
                else:
                    print(f"Command not recognized. Heard: '{command}'. Expected format: 'Launch <game name>'.")
            except sr.UnknownValueError:
                print("Could not understand the command. Please try again.")
            except sr.RequestError:
                print("Could not request results from Google Speech Recognition service.")
            except sr.WaitTimeoutError:
                print("No speech detected. Please try again.")
    
# Example Usage
if __name__ == "__main__":
    game_paths = [
        "C:\\Program Files\\",
        "C:\\Program Files (x86)\\",
        "E:\\Eve\\",
        "E:\\Program Files (x86)\\"
    ]
    scanner = GameScanner(game_paths)
    scanner.scan_for_games()
    
    # Example: Launch game with voice command
    scanner.recognize_speech()