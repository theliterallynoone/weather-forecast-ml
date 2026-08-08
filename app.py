import streamlit as st
from weather import get_weather

st.set_page_config(
    page_title="Weather",
    page_icon="☁️",
    layout="centered"
)
st.title("Weather")
st.write("Get current conditions, wherever you are.")
city = st.text_input(
    "Search",
    placeholder="Enter a city..."
)
if st.button("Get Weather", use_container_width=True):
    if not city:
        st.error("Please enter a city name before requesting a forecast")
    else:
        result = get_weather(city)
        if result.get("success"):
            data = result["data"]
            icon_code = data["weather"][0]["icon"]
            icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png" #https://openweathermap.org/api/weather-conditions#Icon-list
            st.image(icon_url)
            # MAIN WEATHER STUFF
            st.subheader(data.get("name", city))
            st.metric("Temperature", f"{data['main']['temp']} °C", delta=f"Feels like {data['main']['feels_like']} °C") 
            feels_like = data["main"]["feels_like"]
            st.write(f"**Condition:** {data['weather'][0]['description'].title()}")
            # WEATHER DETAILS
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(
                    "Humidity",
                    f"{data['main']['humidity']}%"
                )
            with col2:
                st.metric(
                    "Wind",
                    f"{data['wind']['speed']} m/s"
                )
            with col3:
                st.metric(
                    "Clouds",
                    f"{data['clouds']['all']}%"
                )
        else:
            st.error(result.get("error", "Unable to fetch weather data."))
            status_code = result.get("status_code")
            if status_code:
                st.write(f"Status code: {status_code}")
            