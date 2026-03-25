import streamlit as st
import pickle
import pandas as pd

# Initialize session state
if 'prediction' not in st.session_state:
    st.session_state.prediction = None
if 'cleared' not in st.session_state:
    st.session_state.cleared = False

#Load the trained model
with open("flight_fare_model.pkl", "rb") as f:
    model = pickle.load(f)

# Page config
st.set_page_config(page_title="Flight Fare Predictor", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .main {background-color: white;}
    h1 {
        color: #1f4e79;
        text-align: center;
        font-size: 3em;
        margin-bottom: 0.5em;
    }
    /* Predict button blinking blue */
    div[data-testid="stButton"][key="predict"] > button {
        background-color: #1f4e79;
        color: white;
        font-size: 1.2em;
        padding: 0.5em 2em;
        border-radius: 8px;
        animation: blink 1.5s infinite;
    }
    /* Clear button blinking yellow */
    div[data-testid="stButton"][key="clear"] > button {
        background-color: #FFD700;
        color: black;
        font-size: 1.2em;
        padding: 0.5em 2em;
        border-radius: 8px;
        animation: blink 1.5s infinite;
    }
    @keyframes blink {
        0% {opacity: 1;}
        50% {opacity: 0.6;}
        100% {opacity: 1;}
    }
    /* Right box styling */
    .right-box {
        border: 2px solid #87CEFA;
        border-radius: 10px;
        padding: 20px;
        background-color: #f9fcff;
    }
    /* Prediction output animation */
    .fade-in {animation: fadeIn 2s ease-in-out;}
    @keyframes fadeIn {from {opacity: 0;} to {opacity: 1;}}
    /* Flight emoji animation */
    .plane {
        position: relative;
        animation: fly 12s linear infinite;
        font-size: 40px;
    }
    @keyframes fly {
        0%   {left: -10%;}
        50%  {left: 50%;}
        100% {left: 110%;}
    }
    /* Footer styling */
    footer {visibility: hidden;}
    .footer {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: #1f4e79; color: white;
        text-align: center; padding: 10px; font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# Title + Branding
st.markdown("<h1>✈️ Flight Fare Prediction Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;color:#16324f;'>BESANT TECHNOLOGIES - BTM LAYOUT</h3>", unsafe_allow_html=True)

# Flight emojis animation at the top
st.markdown("<div class='plane'>✈️ ✈️ ✈️</div>", unsafe_allow_html=True)

# Layout: Left for airline/source/destination/stops + buttons, Right for rest
col_left, col_right = st.columns([1,2])

# LEFT PANEL INPUTS
with col_left:
    airline = st.selectbox("Airline", ["IndiGo","Air India","Jet Airways","SpiceJet"])
    source = st.selectbox("Source", ["Delhi","Mumbai","Bangalore","Kolkata"])
    destination = st.selectbox("Destination", ["Cochin","Delhi","Hyderabad","Kolkata"])
    stops = st.selectbox("Total Stops", ["non-stop","1 stop","2 stops","3 stops"])

# RIGHT PANEL INPUTS
with col_right:
    st.markdown("<div class='right-box'>", unsafe_allow_html=True)

    journey_day = st.slider("Journey Day", 1, 31, 1)
    journey_month = st.slider("Journey Month", 1, 12, 1)
    dep_hour = st.slider("Departure Hour", 0, 23, 10)
    dep_min = st.slider("Departure Minute", 0, 59, 30)
    arr_hour = st.slider("Arrival Hour", 0, 23, 14)
    arr_min = st.slider("Arrival Minute", 0, 59, 45)
    duration_mins = st.number_input("Duration (minutes)", min_value=30, step=10, value=255)

    # Flight emojis animation in the middle
    st.markdown("<div class='plane'>✈️ ✈️ ✈️</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# BUTTONS + OUTPUT (below left panel)
with col_left:
    b1, b2 = st.columns(2)

    with b1:
        predict_clicked = st.button("Predict Price", key="predict", help="Click to estimate fare")
    with b2:
        clear_clicked = st.button("Clear", key="clear", help="Reset inputs")

    if predict_clicked:
        input_data = pd.DataFrame({
            'Airline':[airline],
            'Source':[source],
            'Destination':[destination],
            'Total_Stops':[stops],
            'Journey_day':[journey_day],
            'Journey_month':[journey_month],
            'Dep_hour':[dep_hour],
            'Dep_min':[dep_min],
            'Arrival_hour':[arr_hour],
            'Arrival_min':[arr_min],
            'Duration_mins':[duration_mins]
        })
        prediction = model.predict(input_data)
        st.markdown(f"<h4 class='fade-in' style='color:#1f4e79;'>💰 Estimated Flight Fare: ₹ {prediction[0]:.2f}</h4>", unsafe_allow_html=True)

    if clear_clicked:
        st.session_state.prediction = None
        st.session_state.cleared = True

    # Display prediction if it exists
    if st.session_state.prediction is not None:
        st.markdown(f"<h4 class='fade-in' style='color:#1f4e79;'>💰 Estimated Flight Fare: ₹ {st.session_state.prediction:.2f}</h4>", unsafe_allow_html=True)
    
    if st.session_state.cleared:
        st.markdown("<h4 class='fade-in' style='color:#FFD700;'>Inputs cleared! Please re‑enter values.</h4>", unsafe_allow_html=True)

# Footer
st.markdown("<div class='footer'>Designed by K Nagesh</div>", unsafe_allow_html=True)
