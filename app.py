import streamlit as st
from weather import get_weather

st.title("Weather Forecast ML App")
st.write("Enter a city to begin")

city = st.text_input("Enter a city name")

if st.button("Get Weather Forecast"):
    st.write("✅ Button clicked!")
    st.write(f"City = '{city}'")

    if city:
        get_weather(city)

st.write(f"DEBUG: {city}")
if city:
    response = get_weather(city)

    st.write(response)