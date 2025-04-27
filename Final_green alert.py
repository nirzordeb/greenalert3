import streamlit as st
import requests

API_KEY = "45a639fc080aea68034627c083e5b60b"  # Replace with your actual key
DEFAULT_CITY = "Sreemangal"

# Page setup
st.set_page_config(page_title="🌿 GreenAlert – Tea Garden Climate Assistant", layout="centered")

# Set background image from GitHub raw URL
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://raw.githubusercontent.com/nirzordeb/greenalert3/refs/heads/main/bg.jpg");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# === Language Selector ===
language = st.selectbox("🌐 Language / ভাষা বেছে নিন", ["English", "বাংলা"])
bn = language == "বাংলা"

# === Texts ===
texts = {
    "title": "🌿 গ্রিনঅ্যালার্ট – চা বাগানের আবহাওয়া সহকারী" if bn else "🌿 GreenAlert – Tea Garden Climate Assistant",
    "subheader": "বাংলাদেশের চা চাষিদের জন্য স্মার্ট AI পরামর্শ" if bn else "Smart AI Advice for Tea Farmers in Bangladesh",
    "mode_select": "আবহাওয়ার ইনপুট মোড নির্বাচন করুন" if bn else "Choose your mode of weather input",
    "realtime": "রিয়েল-টাইম আবহাওয়া তথ্য" if bn else "Real-Time Data Fetch",
    "manual": "ম্যানুয়াল ইনপুট" if bn else "Manual Input",
    "city_input": "শহরের নাম লিখুন" if bn else "Enter city name",
    "get_weather": "আবহাওয়া দেখুন 🔍" if bn else "🔎 Get Weather Report",
    "weather_for": "{} এর আবহাওয়া" if bn else "✅ Weather for {}",
    "could_not_fetch": "❌ তথ্য আনতে সমস্যা। শহরের নাম বা সংযোগ ঠিক আছে কিনা দেখুন।" if bn else "❌ Could not fetch data. Please check city name or connection.",
    "manual_label": "আবহাওয়ার তথ্য দিন নিচে:" if bn else "Fill in the weather data below:",
    "submit_manual": "🔎 আবহাওয়ার বিশ্লেষণ করুন" if bn else "🔎 Analyze Weather Conditions",
    "suggestion_header": "✅ তথ্য গ্রহণ করা হয়েছে। নিচে পরামর্শ দেওয়া হলো:" if bn else "✅ Data received. Here's what we suggest:"
}

st.title(texts["title"])
st.subheader(texts["subheader"])
st.markdown("##### 🌤️" + (" চা চাষিদের জন্য তাৎক্ষণিক আবহাওয়া তথ্য" if bn else " Real-time AI-Powered Weather Insights for Tea Gardeners"))

option = st.selectbox(texts["mode_select"], [texts["manual"], texts["realtime"]])

# === Weather fetch function ===
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
    except:
        return None

# === Real-Time Mode ===
if option == texts["realtime"]:
    st.markdown("#### 📍 " + texts["city_input"])
    city_input = st.text_input("City", DEFAULT_CITY)

    if st.button(texts["get_weather"]):
        result = fetch_weather(city_input)
        if result:
            st.success(texts["weather_for"].format(result["city"]))
            st.metric("🌡️ " + ("তাপমাত্রা" if bn else "Temperature"), f"{result['temp']} °C")
            st.metric("💧 " + ("আদ্রতা" if bn else "Humidity"), f"{result['humidity']}%")
            st.metric("☁️ " + ("আবহাওয়া" if bn else "Condition"), result["weather"])
            st.metric("🌬️ " + ("বাতাসের গতি" if bn else "Wind Speed"), f"{result['wind']} m/s")
            st.metric("🌧️ " + ("বৃষ্টিপাত" if bn else "Rainfall"), f"{result['rain']} mm")

            # Suggestions
            if result['rain'] > 5:
                st.warning("⚠️ ভারি বৃষ্টিপাত। আজ সেচ দেওয়া বন্ধ রাখুন।" if bn else "⚠️ Heavy rainfall. Avoid irrigation today.")
            elif result['temp'] > 35:
                st.info("🔥 তাপমাত্রা বেশি। গাছ ছায়ায় রাখুন।" if bn else "🔥 High temp. Consider crop shading.")
            elif result['humidity'] < 30:
                st.warning("🌬️ শুষ্ক বাতাস। মাটির আর্দ্রতা পর্যবেক্ষণ করুন।" if bn else "🌬️ Dry air. Monitor soil moisture closely.")
            else:
                st.success("🌱 সব ঠিক আছে! চাষের জন্য আদর্শ আবহাওয়া।" if bn else "🌱 All good! Conditions ideal for farming.")
        else:
            st.error(texts["could_not_fetch"])

# === Manual Input Mode ===
elif option == texts["manual"]:
    st.markdown("#### 📋 " + texts["manual_label"])

    temp = st.number_input("🌡️ " + ("তাপমাত্রা (°C)" if bn else "Temperature (°C)"), min_value=-10.0, max_value=50.0, step=0.1)
    rainfall = st.number_input("🌧️ " + ("বৃষ্টিপাত (mm)" if bn else "Rainfall (mm)"), min_value=0.0, max_value=500.0, step=0.1)
    humidity = st.number_input("💧 " + ("আদ্রতা (%)" if bn else "Humidity (%)"), min_value=0.0, max_value=100.0, step=0.1)

    if st.button(texts["submit_manual"]):
        st.success(texts["suggestion_header"])

        if temp > 35:
            st.warning("🔥 গরম বেশি। বেশি সেচ দিন এবং ছায়া দিন।" if bn else "🔥 It's too hot. Provide crop shading and water frequently.")
        elif temp < 10:
            st.warning("❄️ ঠান্ডা বেশি। গাছ ঢেকে রাখুন।" if bn else "❄️ Cold weather alert. Consider crop covering.")

        if rainfall > 50:
            st.info("🌧️ অতিরিক্ত বৃষ্টি। সেচ বন্ধ রাখুন।" if bn else "🌧️ Heavy rainfall. Delay irrigation and protect low-lying crops.")
        elif rainfall < 5:
            st.info("💦 বৃষ্টির ঘাটতি। সেচ দিন।" if bn else "💦 Not enough rain. Plan irrigation accordingly.")

        if humidity < 30:
            st.warning("🌬️ বাতাস শুষ্ক। পোকামাকড়ের ঝুঁকি বেশি।" if bn else "🌬️ Air is dry. Monitor for pest risk and soil moisture.")
        elif humidity > 80:
            st.info("🌫️ বেশি আদ্রতা। ছত্রাক সংক্রমণ হতে পারে।" if bn else "🌫️ High humidity. Monitor for fungal diseases.")

        if 20 <= temp <= 30 and 30 <= humidity <= 70 and 5 <= rainfall <= 30:
            st.success("✅ চমৎকার আবহাওয়া! চাষের জন্য উপযুক্ত।" if bn else "✅ Excellent weather! Ideal for planting and growth.")

# === Footer ===
st.markdown("---")
st.caption("🚜 " + ("মাঠ পর্যায়ের চাষিদের জন্য বানানো অ্যাপ" if bn else "Built for field-level farmers to input & analyze local weather manually or fetch real-time data."))
st.caption("🚀 Built by team ECO-ECHO (Nirzor & Rudranil)")
st.caption("🌐 Powered by Streamlit + OpenWeatherMap")



