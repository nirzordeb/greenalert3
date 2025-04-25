import streamlit as st
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# Sample dataset
data = {
    'Temperature': [35, 30, 28, 25],
    'Rain': [5, 20, 0, 15],
    'Soil Moisture': ['Low', 'Medium', 'High', 'Low'],
    'Advice': ['Irrigate', 'No irrigation needed', 'Mulch soil', 'Irrigate']
}

df = pd.DataFrame(data)

# Convert soil moisture to numbers
df['Soil Moisture Num'] = df['Soil Moisture'].map({'Low': 0, 'Medium': 1, 'High': 2})

# Model
X = df[['Temperature', 'Rain', 'Soil Moisture Num']]
y = df['Advice']
model = DecisionTreeClassifier().fit(X, y)

# UI
st.title("🌿 GreenAlert – Tea Garden Climate Assistant")
st.write("AI-driven advice for better farming in Sreemangal")

temp = st.slider("Temperature (°C)", 20, 40, 30)
rain = st.slider("Rainfall (mm)", 0, 50, 10)
soil = st.selectbox("Soil Moisture", ['Low', 'Medium', 'High'])

soil_num = {'Low': 0, 'Medium': 1, 'High': 2}[soil]

# Prediction
prediction = model.predict([[temp, rain, soil_num]])[0]
st.success(f"✅ Advice: {prediction}")
