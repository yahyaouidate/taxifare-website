import streamlit as st
import requests
from datetime import datetime

# Titre de la page
st.title("TaxiFareModel Frontend")

st.markdown("""
## Enter ride parameters below
""")

# Champs de saisie
pickup_date = st.date_input("Date of pickup", value=datetime.today())
pickup_time = st.time_input("Time of pickup", value=datetime.now().time())
pickup_datetime = f"{pickup_date} {pickup_time}"

pickup_longitude = st.number_input("Pickup Longitude", value=-73.985428)
pickup_latitude = st.number_input("Pickup Latitude", value=40.748817)
dropoff_longitude = st.number_input("Dropoff Longitude", value=-73.985428)
dropoff_latitude = st.number_input("Dropoff Latitude", value=40.748817)
passenger_count = st.number_input("Passenger Count", min_value=1, max_value=8, value=1)

# API URL
url = 'https://taxifare.lewagon.ai/predict'

# Lorsque l'utilisateur clique sur le bouton
if st.button("Predict fare"):
    params = {
        "pickup_datetime": pickup_datetime,
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": passenger_count
    }

    with st.spinner('Fetching fare prediction...'):
        response = requests.get(url, params=params)

    if response.status_code == 200:
        prediction = response.json().get("fare", "No fare found in response.")
        st.success(f"Estimated fare: ${prediction:.2f}")
    else:
        st.error("API request failed. Please check the URL or parameters.")
