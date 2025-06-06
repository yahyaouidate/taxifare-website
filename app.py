import streamlit as st
import requests
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="NYC Taxi Fare", layout="wide")

# ---- Title Section ----
st.markdown("<h1 style='text-align: center;'>🚕 Need a Wagon? 🚕</h1>", unsafe_allow_html=True)
st.markdown("---")

# ---- Columns ----
col1, col2 = st.columns([2, 3])

with col1:
    st.subheader("📍 Current NYC Weather")
    st.metric("🌡️ Temperature (°C)", "22.8°C")
    st.metric("🌫️ Condition", "Fog")
    st.metric("💨 Wind", "4.3 m/h")

    st.markdown("## 🚖 Fare Prediction")

    pickup_date = st.date_input("Date", value=datetime.today())
    pickup_time = st.time_input("Time", value=datetime.now().time())
    pickup_datetime = f"{pickup_date} {pickup_time}"

    pickup_longitude = st.number_input("Pickup Longitude", value=-73.985428)
    pickup_latitude = st.number_input("Pickup Latitude", value=40.748817)
    dropoff_longitude = st.number_input("Dropoff Longitude", value=-73.985428)
    dropoff_latitude = st.number_input("Dropoff Latitude", value=40.748817)
    passenger_count = st.slider("Passenger Count", 1, 8, 1)

    if st.button("💰 Predict fare"):
        params = {
            "pickup_datetime": pickup_datetime,
            "pickup_longitude": pickup_longitude,
            "pickup_latitude": pickup_latitude,
            "dropoff_longitude": dropoff_longitude,
            "dropoff_latitude": dropoff_latitude,
            "passenger_count": passenger_count
        }

        with st.spinner("Contacting NYC prediction service..."):
            response = requests.get("https://taxifare.lewagon.ai/predict", params=params)

        if response.status_code == 200:
            prediction = response.json().get("fare", None)
            st.success(f"🎯 Estimated fare: ${prediction:.2f}")
        else:
            st.error("API call failed.")

with col2:
    st.subheader("🗺️ Ride Map")
    map_data = pd.DataFrame({
        "lat": [pickup_latitude, dropoff_latitude],
        "lon": [pickup_longitude, dropoff_longitude]
    })
    st.map(map_data)