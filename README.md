
# Weather Predictor using Machine Learning

A machine learning project to predict weather parameters using historical meteorological data.

## Overview
This app is a small weather dashboard built with Streamlit. It lets a user enter a city name, fetches weather data from the OpenWeather API, and displays the result in the browser.
There are three key files- ``` app.py ```, ```weather.py```& ```config.py``` . 

### Heres what each file does
```app.py```: This is the user interface.
It creates the page title and a text input for the city.
When the user clicks the button, it checks whether a city was entered.
It calls the weather function, then shows the weather details such as temperature, feels-like temperature, condition, humidity, and wind speed.

```weather.py```: This handles the API request.
It imports the API key from config.py.
It builds a request URL to OpenWeather with the city name and metric units.
If the request works, it returns the weather data.
If something fails, it returns an error message and status code.

```config.py```: This loads the API key from a .env file.
It uses Python’s dotenv library to read environment variables.
The key it looks for is ~open_weather_api_key~ (shh)

## Tech Stack
- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Streamlit

## Status
🚧 In Progress

(im slow and its not my fault im a 12th grader)
