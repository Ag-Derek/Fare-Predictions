#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# Load your dataset
df = pd.read_csv(r"C:\Users\Ghaidems\Downloads\ghana_ride_sharing_synthetic.csv")

# Select features and target
features = ["city", "pickup_area", "dropoff_area", "duration_min", "distance_km", "rating", "payment_method"]
target = "fare"

X = df[features]
y = df[target]

# Encode categorical variables
label_encoders = {}
for col in ["city", "pickup_area", "dropoff_area", "payment_method"]:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    label_encoders[col] = le

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Mean Absolute Error:", round(mae, 2))
print("R² Score:", round(r2, 3))

# Example prediction
sample_trip = pd.DataFrame({
    "city": ["Accra"],
    "pickup_area": ["Osu"],
    "dropoff_area": ["East Legon"],
    "duration_min": [25],
    "distance_km": [12.3],
    "rating": [4.8],
    "payment_method": ["Card"]
})

# Encode sample trip
for col in ["city", "pickup_area", "dropoff_area", "payment_method"]:
    sample_trip[col] = label_encoders[col].transform(sample_trip[col])

predicted_fare = model.predict(sample_trip)[0]
print(f"\nPredicted Fare: GHS {predicted_fare:.2f}")


# In[5]:


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# Load your dataset
df = pd.read_csv(r"C:\Users\Ghaidems\Downloads\ghana_ride_sharing_synthetic.csv")

# Select features and target
features = ["city", "pickup_area", "dropoff_area", "duration_min", "distance_km", "rating", "payment_method"]
target = "fare"

X = df[features]
y = df[target]

# Encode categorical variables
label_encoders = {}
for col in ["city", "pickup_area", "dropoff_area", "payment_method"]:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    label_encoders[col] = le

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Mean Absolute Error:", round(mae, 2))
print("R² Score:", round(r2, 3))

# Example prediction
sample_trip = pd.DataFrame({
    "city": ["Accra"],
    "pickup_area": ["Osu"],
    "dropoff_area": ["Madina"],
    "duration_min": [25],
    "distance_km": [15.3],
    "rating": [4.8],
    "payment_method": ["Card"]
})
# Encode sample trip
for col in ["city", "pickup_area", "dropoff_area", "payment_method"]:
    sample_trip[col] = label_encoders[col].transform(sample_trip[col])

predicted_fare = model.predict(sample_trip)[0]
print(f"\nPredicted Fare: GHS {predicted_fare:.2f}")


# In[4]:


sample_trip = pd.DataFrame({
    "city": ["Accra"],
    "pickup_area": ["Osu"],
    "dropoff_area": ["Madina"],
    "duration_min": [25],
    "distance_km": [15.3],
    "rating": [4.8],
    "payment_method": ["Card"]
})


# In[6]:


import joblib

# Save model and encoders
joblib.dump(model, "fare_model.pkl")
joblib.dump(label_encoders, "encoders.pkl")

print("✅ Model and encoders saved!")


# In[8]:


import streamlit as st
import pandas as pd
import joblib

# Load model and encoders
model = joblib.load("fare_model.pkl")
encoders = joblib.load("encoders.pkl")

st.title(" Ghana Ride Fare Predictor")

st.write("Enter trip details below to estimate your fare:")

# Input fields
city = st.selectbox("City", encoders["city"].classes_)
pickup = st.selectbox("Pickup Area", encoders["pickup_area"].classes_)
dropoff = st.selectbox("Dropoff Area", encoders["dropoff_area"].classes_)
duration = st.number_input("Trip Duration (minutes)", 1, 60, 20)
distance = st.number_input("Trip Distance (km)", 1.0, 30.0, 10.0)
rating = st.slider("Driver Rating", 3.0, 5.0, 4.5, 0.1)
payment = st.selectbox("Payment Method", encoders["payment_method"].classes_)

# Predict button
if st.button("Predict Fare"):
    # Encode user input
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
    st.success(f" Estimated Fare: GHS {predicted_fare:.2f}")


# In[9]:


streamlit --version


# In[10]:


import os
print(os.getcwd())


# In[ ]:




