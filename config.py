from dotenv import load_dotenv
from pathlib import Path
import os

# Load the .env file from the project directory.
dotenv_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path)

API_KEY = os.getenv("open_weather_api_key")