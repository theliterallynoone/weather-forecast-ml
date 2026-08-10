import streamlit as st
from weather import get_weather

st.set_page_config(
    page_title="Weather",
    page_icon="☁️",
    layout="centered"
)

# --- Minimal Apple-inspired styling kept inside app.py ---
st.markdown(
    """
    <style>
    :root {
      --bg-card: rgba(247,248,250,0.85);
      --muted: #6b7280;
      --accent: #0f172a;
      --card-border: rgba(15,23,42,0.06);
    }
    body, .stApp {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial;
    }
    .header {
      display:flex;
      flex-direction:column;
      align-items:center;
      gap:6px;
      margin-bottom:14px;
    }
    .app-title {
      font-size:20px;
      font-weight:600;
      margin:0;
    }
    .app-sub {
      font-size:13px;
      color:var(--muted);
      margin:0;
    }
    /* Search input + button cohesive styling */
    .search-row .stTextInput>div>div>input {
      padding:10px 12px !important;
      border-radius:10px 0 0 10px !important;
      border:1px solid var(--card-border) !important;
      outline:none !important;
      height:40px;
    }
    .search-row .stButton>button {
      border-radius:0 10px 10px 0 !important;
      padding:10px 14px !important;
      margin:0 !important;
      height:40px;
    }
    .weather-panel{
      display:flex;
      flex-direction:column;
      align-items:center;
      gap:10px;
      margin-top:6px;
    }
    .main-row{
      display:flex;
      align-items:center;
      gap:18px;
      justify-content:center;
      flex-wrap:wrap;
    }
    .ow-icon{
      width:96px;
      height:96px;
    }
    .temp {
      font-size:64px;
      line-height:1;
      font-weight:600;
      color:var(--accent);
    }
    .city {
      font-size:20px;
      color:var(--accent);
      margin-bottom:6px;
    }
    .condition {
      font-size:13px;
      color:var(--muted);
    }
    .cards {
      display:flex;
      gap:12px;
      margin-top:12px;
      flex-wrap:wrap;
      justify-content:center;
    }
    .weather-card{
      background:var(--bg-card);
      border:1px solid var(--card-border);
      border-radius:12px;
      padding:10px 14px;
      min-width:110px;
      text-align:center;
      box-shadow:none;
    }
    .weather-card .label{
      font-size:12px;
      color:var(--muted);
      margin-bottom:6px;
    }
    .weather-card .value{
      font-size:15px;
      font-weight:600;
      color:var(--accent);
    }
    @media (max-width:600px){
      .temp { font-size:48px; }
      .ow-icon { width:80px;height:80px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header
st.markdown(
    '<div class="header"><h1 class="app-title">Weather</h1><div class="app-sub">Get current conditions, wherever you are.</div></div>',
    unsafe_allow_html=True,
)

# Search: put input and button together for cohesive UI
left_col, right_col = st.columns([3, 1], gap="small")
with left_col:
    # Put the input inside the left column so it lines up with the button
    city = st.text_input("Search", placeholder="Enter a city...", key="city_input")
with right_col:
    # Button aligns next to the input and uses the same vertical rhythm
    get_weather_btn = st.button("Get Weather", use_container_width=True)

# Main action
if get_weather_btn:
    if not city:
        st.error("Please enter a city name before requesting a forecast")
    else:
        result = get_weather(city)
        if result.get("success"):
            data = result["data"]
            icon_code = data["weather"][0]["icon"]
            icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"

            # Main weather panel: icon + temperature + condition
            st.markdown('<div class="weather-panel">', unsafe_allow_html=True)
            st.markdown('<div class="main-row">', unsafe_allow_html=True)

            # Icon — use the OpenWeather icon, styled to balance with temperature
            st.markdown(f'<img class="ow-icon" src="{icon_url}" alt="weather icon">', unsafe_allow_html=True)

            # Temperature and supporting text — temperature is the visual focus
            temp = round(data['main']['temp'])
            feels = round(data['main']['feels_like'])
            city_name = data.get('name', city)
            condition = data['weather'][0]['description'].title()
            st.markdown(
                f'<div><div class="city">{city_name}</div>'
                f'<div class="temp">{temp}°C</div>'
                f'<div class="condition">Feels like {feels}° · {condition}</div></div>',
                unsafe_allow_html=True,
            )

            st.markdown('</div>', unsafe_allow_html=True)

            # Subtle information cards: humidity, wind, clouds
            humidity = data['main']['humidity']
            wind = data['wind']['speed']
            clouds = data['clouds']['all']

            st.markdown('<div class="cards">', unsafe_allow_html=True)
            st.markdown(f'<div class="weather-card"><div class="label">Humidity</div><div class="value">{humidity}%</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="weather-card"><div class="label">Wind</div><div class="value">{wind} m/s</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="weather-card"><div class="label">Clouds</div><div class="value">{clouds}%</div></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.error(result.get("error", "Unable to fetch weather data."))
            status_code = result.get("status_code")
            if status_code:
                st.write(f"Status code: {status_code}")
