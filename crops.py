import streamlit as st
import numpy as np
import pandas as pd
import joblib
import requests as req
import json



st.title("🍃CROP SUGGESTER SYSTEM🍃")

model_dt = joblib.load('model_dt')
model_g = joblib.load('model_g')
model_xg = joblib.load('model_xg')

loc = st.text_input("ENTER LOCATION")

soil = st.selectbox(
            "🌏  ENTER THE SOIL TYPE 🌏",
            ('Alluvial',
            'Clay',
            'Loam',
            'black',
            'sandy',
            'laterite',
            'red')
)

output = {

    'rice' : 1,
    'maize' : 2,
    'chickpea' : 3,
    'kidneybeans':4,
    'pigeonpeas' : 5,
    'mothbeans' : 6,
    'mungbean' : 7,
    'blackgram' : 8,
    'lentil' : 9,
    'pomegranate' : 10,
    'banana' : 11,
    'mango' : 12,
    'grapes' : 13,
    'watermelon' : 14,
    'muskmelon' : 15,
    'apple' : 16,
    'orange' : 17,
    'papaya' : 18,
    'coconut': 19,
    'cotton' : 20,
    'jute' : 21,
    'coffee' : 22
}

slt = {
    'Alluvial' : 1,
     'Clay' : 2,
     'Loam' : 3,
    'black' : 4,
    'sandy' : 5,
    'laterite' : 6,
    'red' : 7
}


styp = slt.get(soil)

def crop_suggest(t, h):
    rows = np.array([styp,t,h])
    X = pd.DataFrame([rows])
    pred_dt = model_dt.predict(X)[0]
    pred_g = model_g.predict(X)[0]
    pred_xg = model_xg.predict(X)[0]
    for name, age in output.items():
        if age == pred_xg:
            st.write("THE BEST CROP FOR YOU IS %s"   %(name))
        if pred_xg != pred_g:
            if age == pred_g:
                st.write("THE BEST CROP FOR YOU IS %s"   %(name))
        if pred_g != pred_dt:
            if age == pred_dt:
                st.write("THE BEST CROP FOR YOU IS %s"   %(name))


def location():
    url = "https://api.openweathermap.org/data/2.5/weather?q=" + loc + "&appid=a4e5c8cfa3b320889d90183e5b70150a&units=metric"
    res = req.get(url).json()
    t = float(res['main']['temp'])
    h = float(res['main']['humidity'])
    crop_suggest(t, h)

st.button('PREDICT',on_click = location)
