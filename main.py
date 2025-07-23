import streamlit as st
import pandas as pd
import os
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# ------------------ Load and Train ------------------

@st.cache_data
def load_data():
    path = "data.csv"
    if not os.path.exists(path):
        st.error("❌ data.csv file not found!")
        return None, None
    df = pd.read_csv(path).dropna()
    return df["query"], df["intent"]

@st.cache_resource
def train_model(X, y):
    model = make_pipeline(TfidfVectorizer(), MultinomialNB())
    model.fit(X, y)
    return model

# ------------------ Mock Weather ------------------

def get_weather_response(city):
    weather_data = {
        "Bangalore": "🌧️ It's raining and 28°C in Bangalore.",
        "Mumbai": "🌦️ Light rain in Mumbai.",
        "Delhi": "🔥 Hot and dry with 36°C.",
        "Goa": "☀️ Humid and 32°C with clear skies.",
        "Pune": "🌤️ 25°C with mild breeze in Pune.",
        "Hyderabad": "☁️ It's cloudy in Hyderabad.",
        "Chennai": "⛈️ Thunderstorms expected in Chennai."
    }
    return weather_data.get(city, f"⚠️ No weather data available for {city}.")

# ------------------ Streamlit UI ------------------

st.set_page_config(page_title="Weather Chatbot ☁️", page_icon="🤖")

st.title("🤖 Weather Chatbot")
st.markdown("Ask anything related to weather or just say hi!")

# Load and train
X, y = load_data()
if X is None:
    st.stop()

model = train_model(X, y)

# Input from user
user_input = st.text_input("👤 Your message:")
city = st.selectbox("🌆 Choose a city", [
    "", "Bangalore", "Mumbai", "Delhi", "Goa", "Pune", "Hyderabad", "Chennai"
])

# Chat response
if st.button("Send"):
    if not user_input:
        st.warning("Please enter a message.")
    else:
        intent = model.predict([user_input])[0]
        
        if intent == "greeting":
            st.success("👋 Hello! How can I help you?")
        elif intent == "goodbye":
            st.info("👋 Goodbye! Have a nice day!")
        elif intent == "get_weather":
            if city:
                st.success(get_weather_response(city))
            else:
                st.warning("Please select a city to get the weather.")
        else:
            st.error("🤖 Sorry, I didn’t understand that.")
