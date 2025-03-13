NovaBot

NovaBot is a voice-activated AI assistant designed to perform a variety of tasks such as checking the weather, playing music and movies, launching games, and performing web searches. This project is structured for modularity and easy expansion, making it a great starting point for further development.

Features

Voice Recognition: Uses speech recognition to process commands.

Weather Monitoring: Retrieves current weather conditions.

Music Playback: Plays music via Spotify and Pandora.

Movie Playback: Supports Plex and Emby for streaming.

Game Launching: Detects installed games and launches them.

Web Scraping: Searches the web for information.

Persistent Operation: NovaBot remains active unless explicitly closed.

Installation

Prerequisites

Python 3.9 or newer

Required libraries: speechrecognition, requests, json, subprocess, etc.

A working microphone for voice commands

API keys for OpenWeather and other services (if applicable)

Setup

Clone the repository:

git clone https://github.com/yourusername/NovaBot.git
cd NovaBot

Install dependencies:

pip install -r requirements.txt

Set up API keys in a .env file for weather services.

Run NovaBot:

python main.py

Usage

Once started, NovaBot listens for commands. Some examples include:

"Weather in Marble Falls"

"Play Bohemian Rhapsody on Spotify"

"Launch Diablo 3"

"Watch The Matrix"

"Search Python programming best practices"

To exit, say: "Goodbye," "Bye," "Exit," or "Close"

Contribution

If you'd like to contribute to the public version, feel free to fork the repository and submit pull requests with improvements.

License

This project is open-source, but certain features may remain proprietary to the original developer.

Future Plans

Add more integrations

Improve conversational capabilities

Expand automation features

NovaBot is a starting point for building an intelligent, interactive AI assistant. Have fun coding! 🚀

Final readme edit -- I do plan on adding more modules to this in time, making t a more robust and extensive application overall. Just have fun with it evereyone!

