#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Ride_Prediction.py

import streamlit as st
import pandas as pd
import joblib

# Load model and encoders
model = joblib.load("fare_model.pkl")
encoders = joblib.load("encoders.pkl")

# Load your dataset to build city-area mapping
df = pd.read_csv("ghana_ride_sharing_synthetic.csv")
city_area_map = df.groupby("city")["pickup_area"].unique().to_dict()

st.title("🇬🇭 Ghana Ride Fare Predictor")
st.write("Enter trip details below to estimate your fare:")

# Step 1: City selection
city = st.selectbox("City", list(city_area_map.keys()))

# Step 2: Filter areas for the selected city
areas = sorted(city_area_map[city])
pickup = st.selectbox("Pickup Area", areas)
dropoff = st.selectbox("Dropoff Area", areas)

# Step 3: Other trip details
duration = st.number_input("Trip Duration (minutes)", 1, 60, 20)
distance = st.number_input("Trip Distance (km)", 1.0, 30.0, 10.0)
rating = st.slider("Driver Rating", 3.0, 5.0, 4.5, 0.1)
payment = st.selectbox("Payment Method", encoders["payment_method"].classes_)

# Step 4: Predict fare
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
