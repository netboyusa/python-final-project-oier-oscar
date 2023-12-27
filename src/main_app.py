import streamlit as st
import numpy as np
from data_operations import get_available_pairs, download_data
from plotting import plot_candles, calculate_stochastic, plot_stochastic, plot_combination

def main():

    try:
        st.set_page_config(layout="wide")
        logo_path = 'images/logo.png'

        st.image(logo_path, width=200)

        st.write("Welcome to our website!")
        st.write("Authors: Oscar Rivera Zayas & Oier Etxeberria Loiarte")

        st.markdown("""
	<style>
                    
	.stSelectbox:first-of-type > div[data-baseweb="select"] > div {
	      background-color: pink;
                    color: black;
    	      padding: 3px;
                    width: 200px;
	}
    .st-b8 {
        width: 200px;
        color: black;
    }
            .styled-container {
            background-color: #f0f0f0;
            padding: 10px;
            border-radius: 5px;
        }
    </style>""", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([3, 4, 10])

        with st.container():
            with col1:
                available_pairs = get_available_pairs()

                pair = st.selectbox("Select Currencies:", available_pairs)

                interval = st.selectbox("Select Time Interval (in minutes):", ["1", "5", "15", "30", "60", "240", "1440", "10080", "21600"])
                data = download_data(pair, interval)

                if data.empty:
                    st.warning("Unable to download data")
                    st.stop()

        with st.container():
            with col2:
                start_date = st.date_input("From Date:",
                                        min_value=min(data["date"]),
                                        max_value=max(data["date"]),
                                        value=min(data["date"]))
                
                end_date = st.date_input("To Date",
                                        min_value=min(data["date"]),
                                        max_value=max(data["date"]),
                                        value=max(data["date"]))

                st.write(f"From Date: {start_date}")
                st.write(f"To Date: {end_date}")
        
        with st.container():
            with col3:
                
                stochastic_data = calculate_stochastic(data)
                filtered_data = stochastic_data[(stochastic_data["date"] >= start_date) & (stochastic_data["date"] <= end_date)]

                tab1, tab2, tab3 = st.tabs(["Plot Candles Graph", "Plot Stochastic Graph", "Plot Combination Graph"])

                with tab1:
                    st.plotly_chart(plot_candles(filtered_data), theme="streamlit", use_container_width=True)

                with tab2:
                    st.plotly_chart(plot_stochastic(filtered_data), theme="streamlit", use_container_width=True)

                with tab3:
                    st.plotly_chart(plot_combination(filtered_data), theme="streamlit", use_container_width=True)
            

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
