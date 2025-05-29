import streamlit as st
import pandas as pd
import datetime
from src.config_base import generate_initial_liquidity_data, generate_new_liquidity_point

def initialize_session_state():
    """Initializes Streamlit session state variables."""
    if 'transactions' not in st.session_state:
        st.session_state['transactions'] = pd.DataFrame(columns=[
            "Transaction ID", "Timestamp", "Sending Institution", "Receiving Institution",
            "Corridor", "Amount Sent", "Sending Stablecoin", "Amount Received",
            "Receiving Stablecoin", "Fee", "Priority", "Status"
        ])

    if 'dark_mode' not in st.session_state:
        st.session_state['dark_mode'] = False

    # Initialize liquidity data if not exists
    if 'liquidity_data' not in st.session_state:
        today = datetime.date.today()
        st.session_state['liquidity_data'] = generate_initial_liquidity_data(today, num_days=30)
        # Ensure Timestamp is datetime
        st.session_state['liquidity_data']['Timestamp'] = pd.to_datetime(st.session_state['liquidity_data']['Timestamp'])
        st.cache_data.clear() # Clear cache on initial load

def refresh_liquidity_data(institution, corridor, stablecoin):
    """Simulates real-time data update for liquidity."""
    if institution and stablecoin and corridor:
        with st.spinner("Processing real-time data update..."):
            # Filter data for the selected institution, corridor, and stablecoin
            filtered_data_series = st.session_state['liquidity_data'][
                (st.session_state['liquidity_data']['Institution'] == institution) &
                (st.session_state['liquidity_data']['Corridor'] == corridor) &
                (st.session_state['liquidity_data']['Stablecoin'] == stablecoin)
            ].sort_values(by='Timestamp').set_index('Timestamp')['Net Position']

            if not filtered_data_series.empty:
                last_position = filtered_data_series.iloc[-1]
                # Pass the historical data series to generate_new_liquidity_point to inform its trend/volatility
                new_point = generate_new_liquidity_point(
                    last_position,
                    filtered_data_series, # Pass historical data
                    institution,
                    corridor,
                    stablecoin
                    )
                new_point_df = pd.DataFrame([new_point])

                # Ensure Timestamp is datetime before concatenation
                new_point_df['Timestamp'] = pd.to_datetime(new_point_df['Timestamp'])
                st.session_state['liquidity_data']['Timestamp'] = pd.to_datetime(st.session_state['liquidity_data']['Timestamp'])


                # Append new point and update session state
                st.session_state['liquidity_data'] = pd.concat([st.session_state['liquidity_data'], new_point_df], ignore_index=True)

                # Limit data size (e.g., keep last 1000 rows total across all filters)
                if len(st.session_state['liquidity_data']) > 1000:
                     st.session_state['liquidity_data'] = st.session_state['liquidity_data'].tail(1000).reset_index(drop=True)

                st.success("Simulated real-time data updated!")
                st.cache_data.clear() # Clear cache to re-calculate forecast with new data
            else:
                st.warning("Cannot refresh data: No historical data found for the selected parameters.")
    else:
        st.warning("Please select Institution, Stablecoin, and Corridor to refresh data.") 