import streamlit as st
import pandas as pd
import numpy as np
import uuid
import datetime
from config_base import FX_RATES # Import FX_RATES from config_base

def get_fx_rate(sending_stablecoin, receiving_stablecoin):
    """Retrieves the FX rate between two stablecoins."""
    return FX_RATES.get((sending_stablecoin, receiving_stablecoin), 1.0)

def calculate_fee(amount, priority):
    """Calculates the transaction fee based on amount and priority."""
    base_rate = 0.0001 # 0.01%
    fee = amount * base_rate
    if priority == "High Priority":
        fee *= 1.5 # 50% increase
    return max(fee, 0.01) # Minimum fee

def create_ledger_entry(
    sending_institution, receiving_institution, corridor, amount_sent,
    sending_stablecoin, receiving_stablecoin, priority, fee
):
    """Creates a dictionary representing a ledger entry."""
    tx_id = uuid.uuid4().hex[:8].upper()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fx_rate = get_fx_rate(sending_stablecoin, receiving_stablecoin)
    amount_received = amount_sent * fx_rate

    return {
        "Transaction ID": tx_id,
        "Timestamp": timestamp,
        "Sending Institution": sending_institution,
        "Receiving Institution": receiving_institution,
        "Corridor": corridor,
        "Amount Sent": amount_sent,
        "Sending Stablecoin": sending_stablecoin,
        "Amount Received": round(amount_received, 2), # Round for display
        "Receiving Stablecoin": receiving_stablecoin,
        "Fee": round(fee, 4), # Round fee for display
        "Priority": priority,
        "Status": "Settled Instantly"
    } 