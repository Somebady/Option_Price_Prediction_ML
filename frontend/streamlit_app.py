import os

import streamlit as st
import requests

from enums.enums import min_strike_price, max_strike_price, min_days, min_option_price, max_option_price, max_days
from templates.layout import streamlit_header, streamlit_footer, streamlit_sidebar

# Set the FastAPI endpoint
API_URL = os.getenv("API_URL")


streamlit_sidebar()
# Define the Streamlit app



def isValid(data):
    if None in data.values():
        return False
    if data["opening_price"] < min_strike_price or data["opening_price"] > max_strike_price:
        return False
    if data["closing_price"] < min_strike_price or data["closing_price"] > max_strike_price:
        return False
    if data["strike_price"] < min_strike_price or data["strike_price"] > max_strike_price:
        return False
    if data["option_closing_price"] < min_option_price or data["option_closing_price"] > max_option_price:
        return False
    if data["days_to_expiry"] < min_days or data["days_to_expiry"] > max_days:
        return False
    return True


def main():

    st.header("Option Predictor Pro", divider="grey")
    description = '''Option Predictor Pro forecasts striker put and call option 
    opening prices based on premarket data, aiding in strategic trading decisions.
    '''
    st.markdown(description)

    # Define input fields
    call_option = st.selectbox("Select an option:", ["Call", "Put"], index=0)
    opening_price = st.number_input("Opening Price", min_value=min_strike_price, max_value=max_strike_price, value=None)
    closing_price = st.number_input("Closing Price", min_value=min_strike_price, max_value=max_strike_price, value=None)
    strike_price = st.number_input("Option Strike Price", min_value=min_strike_price, max_value=max_strike_price, value=None)
    option_closing_price = st.number_input("Option Closing Price", min_value=min_option_price, max_value=max_option_price, value=None)
    days_to_expiry = st.number_input("Days Remaining For Next Expiry", min_value=min_days, max_value=max_days, value=None)

    # Collect input data
    data = {
        "option_type": call_option,
        "opening_price": opening_price,
        "closing_price": closing_price,
        "strike_price": strike_price,
        "option_closing_price": option_closing_price,
        "days_to_expiry": days_to_expiry,
    }


    # Disable submit button if there are errors
    submit_button = st.button("Submit")

    if submit_button:
        is_valid = isValid(data)
        if not is_valid:
            st.error("Invalid Input data")
        else:
            # Send data to FastAPI endpoint
            response = requests.post(API_URL, json=data)
            if response.status_code == 200:
                st.success(f"Option with strike price {strike_price} will open at approx. price of {response.json().get('message')}")
            else:
                st.error(response.json().get('detail'))

    st.subheader('Happy Trading :blue[!!] :sunglasses:')

    st.divider()
    st.markdown(
        '**Source Code:**<a href="https://github.com/imakshaysoni/Option_Price_Prediction_ML" target="_blank" class="icon"><img src="https://github.com/favicon.ico" style="margin-left:10px" width="30" height="30"></a>',
        unsafe_allow_html=True)
main()
streamlit_footer()
