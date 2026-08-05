import streamlit as st
from weather import get_weather

st.title("Weather Forecast ML App")
st.write("Enter a city to begin")

city = st.text_input("Enter a city name")

if st.button("Get Weather Forecast"):
    if not city:
        st.error("Please enter a city name before requesting a forecast.")
    else:
        result = get_weather(city)
        if result.get("success"):
            data = result["data"]
            st.subheader(f"Weather in {data.get('name', city)}")
            st.metric("Temperature", f"{data['main']['temp']} °C", delta=f"Feels like {data['main']['feels_like']} °C")
            st.write(f"**Condition:** {data['weather'][0]['description'].title()}")
            st.write(f"**Humidity:** {data['main']['humidity']}%")
            st.write(f"**Wind speed:** {data['wind']['speed']} m/s")
            st.write("### Full API response")
            st.json(data)
        else:
            st.error(result.get("error", "Unable to fetch weather data."))
            status_code = result.get("status_code")
            if status_code:
                st.write(f"Status code: {status_code}")