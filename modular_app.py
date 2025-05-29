import streamlit as st
import pandas as pd
from payments_ui import render_payments_tab
from ledger_ui import render_ledger_tab
from liquidity_ui import render_liquidity_tab
from compliance_ui import render_compliance_tab
from data_manager import initialize_session_state, refresh_liquidity_data

# Set page config
st.set_page_config(
    page_title="StableNet Ledger",
    page_icon="💱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        color: #333333;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff;
        border-radius: 4px 4px 0 0;
        color: #000000;
    }
    .card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
initialize_session_state()

# Sidebar
with st.sidebar:
    st.title("StableNet Ledger")
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    StableNet Ledger is a permissioned DLT platform for instant cross-border payments using stablecoins.
    
    This MVP demonstrates:
    - Instant cross-border payments
    - Transparent ledger
    - AI liquidity forecasting
    - Simulated compliance checks
    """)
    
    st.markdown("---")
    st.markdown("### Demo Mode")
    st.markdown("""
    This is a simulated environment using dummy data. No real transactions are processed.
    """)

# Main content
st.title("StableNet Ledger MVP")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["Payments", "Ledger", "Liquidity Forecast", "Compliance Analytics"])

# Render each tab
with tab1:
    render_payments_tab()

with tab2:
    render_ledger_tab()

with tab3:
    render_liquidity_tab()

with tab4:
    render_compliance_tab()