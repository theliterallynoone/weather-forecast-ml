from dotenv import load_dotenv #from python-dotenv package
import os #from python 
#load the .env file
load_dotenv()
#read the variable
API_KEY = os.getenv("open_weather_api_key")