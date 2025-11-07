#!/usr/bin/env python
# coding: utf-8

# In[ ]:

# Ride_Prediction.py

import streamlit as st
import pandas as pd
import joblib
import math

# ========== HELPER FUNCTION ==========
def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance (in km) between two lat/lon coordinates using Haversine formula."""
    R = 6371  # Earth radius in kilometers
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

# ========== CITY AND ZONE COORDINATES ==========
zone_coords = {
    "Accra": {
        "Airport": (5.6051, -0.1718),
        "Dansoman": (5.5346, -0.2475),
        "East legon": (5.6305, -0.1730),
        "Madina": (5.6689, -0.2197),
        "Osu": (5.5608, -0.1846),
        "Tema": (5.6670, -0.0166)
    },
    "Kumasi": {
        "Adum": (6.6885, -1.6244),
        "Ahodwo": (6.6736, -1.6152),
        "Asokwa": (6.6798, -1.6123),
        "Bantama": (6.7047, -1.6248),
        "Tafo": (6.7254, -1.6129)
    },
    "Takoradi": {
        "Anaji": (4.9041, -1.7769),
        "Effiakuma": (4.9027, -1.7775),
        "Market Circle": (4.8983, -1.7552),
        "Sekondi": (4.9298, -1.7137)
    },
    "Tamale": {
        "Choggu": (9.4184, -0.8361),
        "Lamashegu": (9.4079, -0.8439),
        "Nyohini": (9.4002, -0.8412),
        "Sagnarigu": (9.4225, -0.8503)
    }
}

# ========== LOAD MODEL ==========
model = joblib.load("fare_model.pkl")
encoders = joblib.load("encoders.pkl")

# ========== STREAMLIT UI ==========
st.title("🇬🇭 Ghana Ride Fare Predictor")
st.write("Enter trip details below to estimate your fare:")

# Select City
city = st.selectbox("City", list(zone_coords.keys()))

# Select Pickup and Dropoff filtered by city
pickup = st.selectbox("Pickup Area", list(zone_coords[city].keys()))
dropoff = st.selectbox("Dropoff Area", list(zone_coords[city].keys()))

# Automatically compute distance
pickup_coords = zone_coords[city][pickup]
dropoff_coords = zone_coords[city][dropoff]
distance = haversine_distance(pickup_coords[0], pickup_coords[1], dropoff_coords[0], dropoff_coords[1])

# Other inputs
duration = st.number_input("Trip Duration (minutes)", 1, 60, 20)
rating = st.slider("Driver Rating", 3.0, 5.0, 4.5, 0.1)
payment = st.selectbox("Payment Method", encoders["payment_method"].classes_)

# Prediction
if st.button("Predict Fare"):
    input_df = pd.DataFrame({
        "city": [encoders["city"].transform([city])[0]],
        "pickup_area": [encoders["pickup_area"].transform([pickup])[0]],
        "dropoff_area": [encoders["dropoff_area"].transform([dropoff])[0]],
        "duration_min": [duration],
        "distance_km": [distance],
        "rating": [rating],
        "payment_method": [encoders["payment_method"].transform([payment])[0]]
    })
    predicted_fare = model.predict(input_df)[0]
    st.success(f"Estimated Fare: GHS {predicted_fare:.2f}")
    st.caption(f"Estimated trip distance: {distance:.2f} km (auto-calculated)")
