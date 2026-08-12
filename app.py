import datetime as dt

import streamlit as st
import streamlit.components.v1 as components
import requests

from weather import get_weather
from config import API_KEY

st.set_page_config(
    page_title="Weather",
    page_icon="☁️",
    layout="centered"
)


def get_weather_by_coords(lat, lon):
    if not API_KEY:
        return {
            "success": False,
            "error": "OpenWeather API key is not configured. Add open_weather_api_key to your .env file.",
        }

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return {
            "success": True,
            "data": response.json(),
            "status_code": response.status_code,
        }
    except requests.exceptions.HTTPError as exc:
        try:
            payload = response.json()
            message = payload.get("message", str(exc)) if isinstance(payload, dict) else str(exc)
        except ValueError:
            message = str(exc)
        return {
            "success": False,
            "error": message,
            "status_code": response.status_code,
        }
    except requests.exceptions.RequestException as exc:
        return {
            "success": False,
            "error": str(exc),
            "status_code": getattr(exc.response, "status_code", None),
        }


def get_browser_location():
    """Ask the browser for the user's approximate coordinates. Streamlit Python cannot access GPS directly."""
    html = """
    <script>
      function send(payload) {
        Streamlit.setComponentValue(payload);
      }

      if (!navigator.geolocation) {
        send({ ok: false, error: 'Geolocation is not supported by this browser.' });
      } else {
        navigator.geolocation.getCurrentPosition(
          function(position) {
            send({
              ok: true,
              lat: position.coords.latitude,
              lon: position.coords.longitude,
            });
          },
          function(error) {
            send({
              ok: false,
              error: error.message || 'Location access was denied.'
            });
          },
          { enableHighAccuracy: false, timeout: 10000, maximumAge: 600000 }
        );
      }
    </script>
    """
    return components.html(html, height=0)


def get_local_time_for_city(timezone_seconds):
    tz = dt.timezone(dt.timedelta(seconds=timezone_seconds))
    return dt.datetime.now(dt.timezone.utc).astimezone(tz)


def get_time_period_for_city(timezone_seconds):
    hour = get_local_time_for_city(timezone_seconds).hour
    if 5 <= hour < 11:
        return "morning"
    if 11 <= hour < 17:
        return "daytime"
    if 17 <= hour < 21:
        return "evening"
    return "night"


def classify_weather_condition(main_condition, description):
    text = f"{main_condition or ''} {description or ''}".lower()

    if "thunder" in text or "storm" in text:
        return "thunderstorm"
    if "snow" in text:
        return "snow"
    if "rain" in text or "drizzle" in text:
        return "rain"
    if "cloud" in text or "overcast" in text:
        return "clouds"
    if "clear" in text:
        return "clear"
    return "other"


def get_background_theme(weather_family, time_period):
    themes = {
        ("clear", "morning"): {"background": "linear-gradient(180deg, #f7f0e3 0%, #f3f7fb 100%)", "card_bg": "rgba(255,255,255,0.58)", "card_border": "rgba(15,23,42,0.08)"},
        ("clear", "daytime"): {"background": "linear-gradient(180deg, #edf8ff 0%, #f7fbff 100%)", "card_bg": "rgba(255,255,255,0.60)", "card_border": "rgba(15,23,42,0.08)"},
        ("clear", "evening"): {"background": "linear-gradient(180deg, #f4d9c2 0%, #edf1f8 100%)", "card_bg": "rgba(255,255,255,0.56)", "card_border": "rgba(15,23,42,0.08)"},
        ("clear", "night"): {"background": "linear-gradient(180deg, #0d1b2a 0%, #1a2a3a 100%)", "card_bg": "rgba(255,255,255,0.10)", "card_border": "rgba(255,255,255,0.15)"},
        ("clouds", "daytime"): {"background": "linear-gradient(180deg, #e7edf3 0%, #f5f7fa 100%)", "card_bg": "rgba(255,255,255,0.60)", "card_border": "rgba(15,23,42,0.08)"},
        ("clouds", "night"): {"background": "linear-gradient(180deg, #1c2430 0%, #2d3745 100%)", "card_bg": "rgba(255,255,255,0.10)", "card_border": "rgba(255,255,255,0.12)"},
        ("rain", "daytime"): {"background": "linear-gradient(180deg, #dfe8ef 0%, #d5dfe9 100%)", "card_bg": "rgba(255,255,255,0.58)", "card_border": "rgba(15,23,42,0.08)"},
        ("rain", "night"): {"background": "linear-gradient(180deg, #19242d 0%, #243848 100%)", "card_bg": "rgba(255,255,255,0.10)", "card_border": "rgba(255,255,255,0.12)"},
        ("snow", "daytime"): {"background": "linear-gradient(180deg, #edf7ff 0%, #f4f8fb 100%)", "card_bg": "rgba(255,255,255,0.60)", "card_border": "rgba(15,23,42,0.08)"},
        ("snow", "night"): {"background": "linear-gradient(180deg, #1a2331 0%, #2a3a48 100%)", "card_bg": "rgba(255,255,255,0.10)", "card_border": "rgba(255,255,255,0.12)"},
        ("thunderstorm", "daytime"): {"background": "linear-gradient(180deg, #cfd5dc 0%, #bcc7d1 100%)", "card_bg": "rgba(255,255,255,0.58)", "card_border": "rgba(15,23,42,0.08)"},
        ("thunderstorm", "night"): {"background": "linear-gradient(180deg, #151b25 0%, #222d38 100%)", "card_bg": "rgba(255,255,255,0.10)", "card_border": "rgba(255,255,255,0.12)"},
        ("other", "daytime"): {"background": "linear-gradient(180deg, #eef2f5 0%, #f6f7fb 100%)", "card_bg": "rgba(255,255,255,0.60)", "card_border": "rgba(15,23,42,0.08)"},
        ("other", "night"): {"background": "linear-gradient(180deg, #171d27 0%, #2a3342 100%)", "card_bg": "rgba(255,255,255,0.10)", "card_border": "rgba(255,255,255,0.12)"},
    }

    return themes.get((weather_family, time_period), themes[("clear", "daytime")])


def apply_background_theme(theme):
    st.markdown(
        f"""
        <style>
        body, .stApp {{
            background: {theme['background']};
            transition: background 0.25s ease;
        }}
        .weather-card {{
            background: {theme['card_bg']} !important;
            border-color: {theme['card_border']} !important;
            box-shadow: none !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_weather(data):
    data = data or {}
    weather = (data.get("weather") or [{}])[0]
    icon_code = weather.get("icon")
    icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png" if icon_code else ""

    temp = round(data.get("main", {}).get("temp", 0))
    feels = round(data.get("main", {}).get("feels_like", 0))
    city_name = data.get("name", "City")
    timezone_seconds = data.get("timezone", 0)
    local_time = get_local_time_for_city(timezone_seconds)
    local_time_label = local_time.strftime("%H:%M")
    weather_family = classify_weather_condition(weather.get("main"), weather.get("description"))
    time_period = get_time_period_for_city(timezone_seconds)
    apply_background_theme(get_background_theme(weather_family, time_period))

    st.markdown('<div class="weather-panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="city">{city_name}</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-row">', unsafe_allow_html=True)
    if icon_url:
        st.markdown(f'<img class="ow-icon" src="{icon_url}" alt="weather icon">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="temp-block"><div class="temp">{temp}°C</div><div class="feels-like">Feels like {feels}°C</div><div class="local-time">Local time · {local_time_label}</div></div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    humidity = data.get("main", {}).get("humidity", 0)
    wind = data.get("wind", {}).get("speed", 0)
    clouds = data.get("clouds", {}).get("all", 0)

    st.markdown('<div class="cards">', unsafe_allow_html=True)
    st.markdown(f'<div class="weather-card"><div class="label">Humidity</div><div class="value">{humidity}%</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="weather-card"><div class="label">Wind</div><div class="value">{wind} m/s</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="weather-card"><div class="label">Clouds</div><div class="value">{clouds}%</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


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
      justify-content:center;
      width:100%;
      max-width:560px;
      margin:16px auto 0;
      text-align:center;
    }
    .city {
      font-size:20px;
      font-weight:600;
      letter-spacing:0.12em;
      text-transform:uppercase;
      color:var(--accent);
      margin-bottom:10px;
      width:100%;
      text-align:center;
    }
    .main-row{
      display:flex;
      align-items:center;
      justify-content:center;
      gap:18px;
      flex-wrap:nowrap;
      margin:0 auto;
      width:100%;
    }
    .ow-icon{
      width:96px;
      height:96px;
      display:block;
      flex-shrink:0;
      margin:0 auto;
    }
    .temp-block {
      display:flex;
      flex-direction:column;
      align-items:center;
      justify-content:center;
      min-width:0;
    }
    .temp {
      font-size:68px;
      line-height:0.95;
      letter-spacing:-0.06em;
      font-weight:600;
      color:var(--accent);
      text-align:center;
    }
    .feels-like {
      font-size:14px;
      color:var(--muted);
      margin-top:6px;
      text-align:center;
    }
    .local-time {
      font-size:12px;
      color:var(--muted);
      margin-top:4px;
      text-align:center;
    }
    .cards {
      display:flex;
      gap:12px;
      margin-top:18px;
      flex-wrap:wrap;
      justify-content:center;
      width:100%;
      max-width:560px;
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
      .main-row { flex-wrap:nowrap; gap:10px; }
      .temp { font-size:52px; }
      .ow-icon { width:76px;height:76px; }
      .temp-block { align-items:center; }
      .feels-like { text-align:center; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    '<div class="header"><h1 class="app-title">Weather</h1><div class="app-sub">Get current conditions, wherever you are.</div></div>',
    unsafe_allow_html=True,
)

with st.form(key="weather_form"):
    left_col, right_col = st.columns([3, 1], gap="small")
    with left_col:
        city = st.text_input("Search", placeholder="Enter a city...", key="city_input")
    with right_col:
        get_weather_btn = st.form_submit_button("Get Weather Forecast", use_container_width=True)

location_btn = st.button("Use my location")

if location_btn:
    location = get_browser_location()
    if location and location.get("ok"):
        result = get_weather_by_coords(location["lat"], location["lon"])
        if result.get("success"):
            render_weather(result["data"])
        else:
            st.error(result.get("error", "Unable to fetch weather data."))
            status_code = result.get("status_code")
            if status_code:
                st.write(f"Status code: {status_code}")
    else:
        st.warning(location.get("error", "Location access was denied. Please search by city instead.") if location else "Location access was denied. Please search by city instead.")

elif get_weather_btn:
    city = (city or "").strip()
    if not city:
        st.error("Please enter a city name before requesting a forecast")
    else:
        result = get_weather(city)
        if result.get("success"):
            render_weather(result["data"])
        else:
            st.error(result.get("error", "Unable to fetch weather data."))
            status_code = result.get("status_code")
            if status_code:
                st.write(f"Status code: {status_code}")
