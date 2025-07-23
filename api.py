import streamlit as st
import requests
from datetime import datetime

# ✅ OpenWeatherMap API Key
API_KEY = 'd8b6465df2b1d9029296c65e5eaa1dad'

# ✅ Get current weather
def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()

        return {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temp": round(data["main"]["temp"]),
            "feels_like": round(data["main"]["feels_like"]),
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "wind": round(data["wind"]["speed"] * 3.6),
            "condition": data["weather"][0]["description"].title(),
            "icon": data["weather"][0]["icon"],
            "visibility": data.get("visibility", 10000) // 1000,
            "sunrise": datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M"),
            "sunset": datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M")
        }
    except:
        return None

# ✅ Get 5-day forecast
def get_forecast(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        forecast = []
        for entry in data["list"]:
            dt = datetime.fromtimestamp(entry["dt"]).strftime("%d %b %H:%M")
            forecast.append(f"{dt}: {entry['main']['temp']}°C, {entry['weather'][0]['description'].title()}")
        return forecast[:10]
    except:
        return []

# ✅ Travel advice
def travel_tip(city, temp, condition):
    tips = []

    if "rain" in condition.lower():
        tips.append("☔ It's rainy — carry an umbrella or raincoat.")
    elif temp < 10:
        tips.append("🧥 Cold weather — pack jackets and warm clothes.")
    elif temp > 30:
        tips.append("😎 Hot weather — wear cotton clothes and stay hydrated.")
    else:
        tips.append("🌞 Pleasant weather — perfect for travel!")

    month = datetime.now().month
    best_time = {
        "Shimla": "March to June",
        "Ooty": "April to June",
        "Jaipur": "October to March",
        "Goa": "November to February",
        "Kerala": "October to March",
        "Kanyakumari": "October to March",
        "Darjeeling": "March to May",
        "Manali": "March to June",
        "Udaipur": "September to March"
    }

    suggestions = {
        "Kanyakumari": ["Vivekananda Rock", "Sunset Point", "Kanyakumari Beach"],
        "Darjeeling": ["Tiger Hill", "Batasia Loop", "Tea Gardens"],
        "Manali": ["Rohtang Pass", "Solang Valley", "Old Manali"],
        "Udaipur": ["City Palace", "Lake Pichola", "Bagore Ki Haveli"]
    }

    hotels = {
        "Kanyakumari": ["Hotel Seaview", "Sparsa Resort", "The Gopinivas Grand"],
        "Darjeeling": ["Mayfair Darjeeling", "Hotel Seven Seventeen", "Summit Swiss Heritage Hotel"],
        "Manali": ["The Himalayan", "Snow Valley Resorts", "Johnson Lodge"],
        "Udaipur": ["Taj Lake Palace", "Trident Udaipur", "Hotel Lakend"]
    }

    city_title = city.title()
    rec = suggestions.get(city_title, [])
    stay = hotels.get(city_title, [])

    if city_title in best_time:
        rec.append(f"Best time to visit: {best_time[city_title]}")

    return tips, rec, stay

# ✅ Background and Font Styling
st.set_page_config(layout="wide", page_title="Travel Weather Assistant")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-image: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=2100&q=80');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
h1, h2, h3, p, .stMarkdown {
    color: #ffffff;
    font-family: 'Segoe UI', sans-serif;
}
.stTextInput > div > div > input {
    background-color: #ffffff22;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ✅ Title
st.markdown("<h1 style='text-align:center;'>🏖️ Travel & Weather Guide</h1>", unsafe_allow_html=True)

# ✅ Input
city = st.text_input("📍 Enter a popular travel city (e.g., Goa, Jaipur, Shimla):")

if city:
    weather = get_weather(city)
    forecast = get_forecast(city)

    if weather:
        st.image(f"http://openweathermap.org/img/wn/{weather['icon']}@2x.png", width=100)

        st.markdown(f"""
        <div style="background-color: rgba(0,0,0,0.5); padding: 20px; border-radius: 15px;">
            <h2>📌 {weather['city']}, {weather['country']}</h2>
            <p><b>🌡️ Temperature:</b> {weather['temp']}°C (Feels like {weather['feels_like']}°C)</p>
            <p><b>🌤️ Condition:</b> {weather['condition']}</p>
            <p><b>💧 Humidity:</b> {weather['humidity']}%</p>
            <p><b>🌬️ Wind:</b> {weather['wind']} km/h</p>
            <p><b>👀 Visibility:</b> {weather['visibility']} km</p>
            <p><b>📈 Pressure:</b> {weather['pressure']} hPa</p>
            <p><b>🌅 Sunrise:</b> {weather['sunrise']} | <b>🌇 Sunset:</b> {weather['sunset']}</p>
        </div>
        """, unsafe_allow_html=True)

        tips, recs, stays = travel_tip(city, weather["temp"], weather["condition"])

        st.markdown("### 🧠 AI Travel Suggestions")
        for tip in tips:
            st.success(tip)

        if recs:
            st.markdown("### 📍 Top Attractions")
            for r in recs:
                st.info(f"✅ {r}")

        if stays:
            st.markdown("### 🏨 Recommended Hotels")
            for h in stays:
                st.warning(f"🏠 {h}")

        if forecast:
            st.markdown("### 📅 4–5 Day Forecast")
            for line in forecast:
                st.caption(f"🔮 {line}")

    else:
        st.error("❌ Could not retrieve weather. Check city name or try later.")






