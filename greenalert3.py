import streamlit as st
import requests






# Language switcher
language = st.selectbox("Select Language / ভাষা বেছে নিন", ["English", "বাংলা"])

# Translations Dictionary
translations = {
    "English": {
        "title": "Future Weather Forecast App",
        "city_prompt": "Enter City Name",
        "current_weather": "Current Weather of",
        "temperature": "Temperature",
        "humidity": "Humidity",
        "rainfall": "Rainfall",
        "description": "Weather Description",
        "not_found": "City not found. Please enter a valid city.",
        "enter_city": "Please enter a city name.",
        "forecast": "Weather Forecast",
        "manual_input": "Manual Input for Farmers",
        "temp_label": "Temperature (°C)",
        "humidity_label": "Humidity (%)",
        "rainfall_label": "Rainfall (mm)",
        "summary": "According to your input:"
    },
    "বাংলা": {
        "title": "ভবিষ্যতের আবহাওয়া পূর্বাভাস অ্যাপ",
        "city_prompt": "শহরের নাম লিখুন",
        "current_weather": "বর্তমান আবহাওয়া",
        "temperature": "তাপমাত্রা",
        "humidity": "আর্দ্রতা",
        "rainfall": "বৃষ্টিপাত",
        "description": "আবহাওয়ার বিবরণ",
        "not_found": "শহরের তথ্য পাওয়া যায়নি। দয়া করে শহরের নাম ঠিক মত লিখুন।",
        "enter_city": "অনুগ্রহ করে একটি শহরের নাম লিখুন।",
        "forecast": "আবহাওয়া পূর্বাভাস",
        "manual_input": "কৃষকদের জন্য ইনপুট:",
        "temp_label": "তাপমাত্রা (°C)",
        "humidity_label": "আর্দ্রতা (%)",
        "rainfall_label": "বৃষ্টিপাত (মিমি)",
        "summary": "তথ্য অনুযায়ী:"
    }
}

t = translations[language]
































# === CONFIGURATION ===
API_KEY = "45a639fc080aea68034627c083e5b60b"  # Replace with your actual key
DEFAULT_CITY = "Sreemangal"

# === PAGE DESIGN ===
st.set_page_config(page_title="🌿 GreenAlert – Tea Garden Climate Assistant", layout="centered")


st.markdown("""
    <style>
    .main {
        background-image: url('https://i.ibb.co/DkgM1w5/green-bg.jpg');
        background-size: cover;
        padding: 2rem;
        border-radius: 10px;
        color: white;
    }
    h1 {
        color: #ffffff;
        text-align: center;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# === APP HEADER ===
st.title("🌿 GreenAlert – Tea Garden Climate Assistant")
st.subheader("Smart AI Advice for Tea Farmers in Bangladesh")
st.markdown("##### Real-time AI-Powered Weather Insights for Tea Gardeners & Farmers ")

# === USER CHOICE ===
option = st.selectbox("Choose your mode of weather input", ["Manual Input", "Real-Time Data Fetch"])

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

# === REAL-TIME DATA SECTION ===
if option == "Real-Time Data Fetch":
    st.markdown("#### 📍 Enter city name to get real-time weather data")
    city_input = st.text_input("City", DEFAULT_CITY)

    if st.button("🔎 Get Weather Report"):
        result = fetch_weather(city_input)
        if result:
            st.success(f"✅ Weather for {result['city']}")
            st.metric("🌡️ Temperature", f"{result['temp']} °C")
            st.metric("💧 Humidity", f"{result['humidity']}%")
            st.metric("☁️ Condition", result["weather"])
            st.metric("🌬️ Wind Speed", f"{result['wind']} m/s")
            st.metric("🌧️ Rainfall", f"{result['rain']} mm (last hour)")

            # === AI-LIKE SUGGESTIONS ===
            if result['rain'] > 5:
                st.warning("⚠️ Heavy rainfall. Avoid irrigation today.")
            elif result['temp'] > 35:
                st.info("🔥 High temp. Consider crop shading.")
            elif result['humidity'] < 30:
                st.warning("🌬️ Dry air. Monitor soil moisture closely.")
            else:
                st.success("🌱 All good! Conditions ideal for farming.")
        else:
            st.error("❌ Could not fetch data. Please check city name or connection.")

# === MANUAL INPUT SECTION ===
elif option == "Manual Input":
    st.markdown("#### 📋 Fill in the weather data below:")

    # Manual input fields
    temp = st.number_input("🌡️ Temperature (°C)", min_value=-10.0, max_value=50.0, step=0.1)
    rainfall = st.number_input("🌧️ Rainfall (mm)", min_value=0.0, max_value=500.0, step=0.1)
    humidity = st.number_input("💧 Humidity (%)", min_value=0.0, max_value=100.0, step=0.1)

    if st.button("🔎 Analyze Weather Conditions"):
        st.success("✅ Data received. Here's what we suggest:")

        # === SUGGESTIONS BASED ON MANUAL INPUT ===
        if temp > 35:
            st.warning("🔥 It's too hot. Provide crop shading and water frequently.")
        elif temp < 10:
            st.warning("❄️ Cold weather alert. Consider crop covering.")

        if rainfall > 50:
            st.info("🌧️ Heavy rainfall. Delay irrigation and protect low-lying crops.")
        elif rainfall < 5:
            st.info("💦 Not enough rain. Plan irrigation accordingly.")

        if humidity < 30:
            st.warning("🌬️ Air is dry. Monitor for pest risk and soil moisture.")
        elif humidity > 80:
            st.info("🌫️ High humidity. Monitor for fungal diseases.")

        if 20 <= temp <= 30 and 30 <= humidity <= 70 and 5 <= rainfall <= 30:
            st.success("✅ Excellent weather! Ideal for planting and growth.")

st.markdown("---")
st.caption("🚜 Built for field-level farmers to input & analyze local weather manually or fetch real-time data.")
st.caption("""🚀 Built by team ECO-ECHO (Nirzor & Rudranil)""")
st.caption("🚀 Powered by Streamlit + OpenWeatherMap")

