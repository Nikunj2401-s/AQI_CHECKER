import streamlit as st
import requests

# API Keys
WAQI_API_KEY = "7387aff0c7e2db1b2f62582a324e80bb53b9b4ee"
OPENWEATHER_API_KEY = "769acf1b4c85d57ec3c7f4593141a822"

# Helper Functions
def get_aqi(city):
    url = f"https://api.waqi.info/feed/{city}/?token={WAQI_API_KEY}"
    response = requests.get(url).json()
    if response.get("status") == "ok":
        return response["data"]["aqi"]
    return None

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url).json()
    if response.get("cod") == 200:
        return {
            "temp": response["main"]["temp"],
            "description": response["weather"][0]["description"].title(),
            "humidity": response["main"]["humidity"],
            "wind_speed": response["wind"]["speed"]
        }
    return None

def aqi_quality(aqi):
    if aqi is None:
        return "Unknown"
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups"
    elif aqi <= 200:
        return "Unhealthy"
    elif aqi <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"

# Streamlit App
st.set_page_config(page_title="AQI Checker", layout="centered")
st.title("🌫️ AQI Checker – Check Air Quality & Weather")

city = st.text_input("Enter a city name:")

if st.button("Check Now") and city:
    aqi = get_aqi(city)
    quality = aqi_quality(aqi)
    weather = get_weather(city)

    if aqi is None:
        st.error("⚠️ AQI data not available for this location.")
    else:
        st.subheader(f"AQI in {city.title()}: {aqi} ({quality})")

        if weather:
            st.markdown("### 🌦️ Weather Info:")
            st.write(f"🌡️ Temperature: {weather['temp']} °C")
            st.write(f"🌬️ Wind Speed: {weather['wind_speed']} m/s")
            st.write(f"💧 Humidity: {weather['humidity']}%")
            st.write(f"🌤️ Description: {weather['description']}")
        else:
            st.warning("Weather data not available.")
