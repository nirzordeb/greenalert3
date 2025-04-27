# Final GreenAlert Combined App
# Includes: Real-Time Weather + Manual Input + Language Support + Background Image + Team Info

import streamlit as st
import requests
import base64

# === CONFIGURATION ===
API_KEY = "45a639fc080aea68034627c083e5b60b"  # <-- Put your API key here
DEFAULT_CITY = "Sreemangal"

# === BACKGROUND IMAGE ===
def set_bg_from_local(Al-bg.jpg):
    with open(Al-bg.jpg, "rb") as f:
        encoded_string = base64.b64encode(f.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:Al-bg.jpg;base64,{encoded_string.decode()}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set page config
st.set_page_config(page_title="GreenAlert - Tea Garden Climate Assistant", layout="wide")

# Add Background
set_bg_from_local("Al-bg.jpg")  # make sure background.jpg is in same folder

# === LANGUAGE SETUP ===
language = st.selectbox("🌐 Language / ভাষা বেছে নিন", ["English", "বাংলা"])
bn = language == "বাংলা"

# === TEXT DICTIONARY ===
texts = {
    "title": "🌿 গ্রিনঅ্যালার্ট" if bn else "🌿 GreenAlert",
    "subtitle": "চা বাগানের জন্য AI আবহাওয়া সহকারী" if bn else "AI-Powered Climate Assistant for Tea Gardens",
    "choose_mode": "আবহাওয়ার ইনপুট নির্বাচন করুন" if bn else "Choose Your Mode",
    "manual": "ম্যানুয়াল ইনপুট" if bn else "Manual Input",
    "realtime": "রিয়েল-টাইম আবহাওয়া" if bn else "Real-Time Weather",
    "city_prompt": "শহরের নাম লিখুন" if bn else "Enter City Name",
    "get_weather": "আবহাওয়া দেখুন 🔍" if bn else "🔍 Get Weather",
    "manual_prompt": "নিজে ইনপুট দিন:" if bn else "Enter Data Manually:",
    "analyze": "বিশ্লেষণ করুন" if bn else "Analyze",
    "team_header": "👥 টিম ইকো-ইকো" if bn else "👥 Team Eco-Echo"
}

# === HEADER ===
st.title(texts["title"])
st.subheader(texts["subtitle"])

# === TEAM INFO in SIDEBAR ===
st.sidebar.header(texts["team_header"])
st.sidebar.markdown("""
**Nirzor Deb**  
Leader, Team Eco-Echo  
Dhaka Residential Model College  
01733987514 | debkanchan437@gmail.com

**Rudronil Das**  
Senior Developer, Team Eco-Echo  
Engineering University School and College  
01533311182 | drudra339@gmail.com
""")

# === FUNCTION TO FETCH WEATHER ===
def fetch_weather(city_name):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {
                "city": data["name"],
                "temp": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "weather": data["weather"][0]["description"].title(),
                "rain": data.get("rain", {}).get("1h", 0),
                "wind": data["wind"]["speed"]
            }
        else:
            return None
    except:
        return None

# === USER MODE SELECTION ===
mode = st.selectbox(texts["choose_mode"], [texts["manual"], texts["realtime"]])

# === REAL-TIME WEATHER SECTION ===
if mode == texts["realtime"]:
    st.markdown(f"#### {texts['city_prompt']}")
    city_input = st.text_input("City", DEFAULT_CITY)
    
    if st.button(texts["get_weather"]):
        result = fetch_weather(city_input)
        if result:
            st.success(f"✅ {result['city']}")
            st.metric("🌡️ Temperature", f"{result['temp']} °C")
            st.metric("💧 Humidity", f"{result['humidity']}%")
            st.metric("☁️ Condition", result["weather"])
            st.metric("🌬️ Wind Speed", f"{result['wind']} m/s")
            st.metric("🌧️ Rainfall", f"{result['rain']} mm")

            if result['rain'] > 5:
                st.warning("⚠️ Heavy Rainfall. Manage drainage.")
            elif result['temp'] > 35:
                st.warning("🔥 High Temp. Shade needed.")
            elif result['humidity'] < 30:
                st.warning("💨 Low Humidity. Watch soil moisture.")
            else:
                st.success("✅ Good weather for farming!")
        else:
            st.error("❌ Could not fetch weather. Check city or API key.")

# === MANUAL INPUT SECTION ===
elif mode == texts["manual"]:
    st.markdown(f"#### {texts['manual_prompt']}")
    temp = st.number_input("🌡️ Temperature (°C)", min_value=-10.0, max_value=50.0, step=0.1)
    humidity = st.number_input("💧 Humidity (%)", min_value=0.0, max_value=100.0, step=0.1)
    rainfall = st.number_input("🌧️ Rainfall (mm)", min_value=0.0, max_value=500.0, step=0.1)
    wind = st.number_input("🌬️ Wind Speed (m/s)", min_value=0.0, max_value=100.0, step=0.1)

    if st.button(texts["analyze"]):
        st.success("✅ Analysis Complete:")

        if temp > 35:
            st.warning("🔥 High Temp. Shade plants!")
        if humidity < 30:
            st.warning("💨 Low Humidity. Increase irrigation.")
        if rainfall > 50:
            st.warning("🌧️ Heavy Rain. Prepare drainage.")
        if wind > 40:
            st.warning("🌬️ High winds. Protect crops!")
        if 20 <= temp <= 30 and 40 <= humidity <= 70 and rainfall < 20:
            st.success("🌱 Excellent growing conditions!")

# === FOOTER ===
st.markdown("""
---
 🎗️Powered by Streamlit X Openwaether map | Developed by Team Eco-Echo (Nirzor & Rudronil)
""")
