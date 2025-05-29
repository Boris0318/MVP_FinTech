import datetime
import pandas as pd
import numpy as np

# Define a mapping of Institutions, Stablecoins, and relevant Corridors
# **Restricted to EUR-NGN and USD-MXN, and USDC/EURC as requested**
institution_stablecoin_corridors = {
    "FinTech A": {
        "USDC": ["USD-MXN"], # Only relevant corridor
        "EURC": ["EUR-NGN"], # Only relevant corridor
    },
    "PSP Alpha": {
        "USDC": ["USD-MXN"], # Only relevant corridor
        "EURC": ["EUR-NGN"], # Only relevant corridor
    },
    "Bank B Mexico": {
        "EURC": ["EUR-NGN"], # Only relevant corridor
        "USDC": ["USD-MXN"], # Only relevant corridor
    },
     "FinTech Omega Nigeria": {
        "EURC": ["EUR-NGN"], # Only relevant corridor
     }
}

# Adjusted base positions and introduced trends/volatility for the restricted set
base_positions_and_trends = {
    # FinTech A
    ("FinTech A", "USDC", "USD-MXN"): {"base": 40000, "trend_per_day": -800, "volatility": 3000},
    ("FinTech A", "EURC", "EUR-NGN"): {"base": 15000, "trend_per_day": 200, "volatility": 2000},

    # PSP Alpha
    ("PSP Alpha", "USDC", "USD-MXN"): {"base": -10000, "trend_per_day": -1000, "volatility": 4000}, # Stronger trend for potential shortfall
    ("PSP Alpha", "EURC", "EUR-NGN"): {"base": 25000, "trend_per_day": 300, "volatility": 2200},

    # Bank B Mexico
    ("Bank B Mexico", "EURC", "EUR-NGN"): {"base": 60000, "trend_per_day": -600, "volatility": 3500}, # Higher base for potential surplus
    ("Bank B Mexico", "USDC", "USD-MXN"): {"base": 30000, "trend_per_day": 400, "volatility": 2800},

    # FinTech Omega Nigeria
    ("FinTech Omega Nigeria", "EURC", "EUR-NGN"): {"base": 8000, "trend_per_day": 150, "volatility": 1500},
}

# Dummy Liquidity Data (Initial 30 days - Simulated)
def generate_initial_liquidity_data(start_date, num_days=30):
    data = []
    institutions = list(institution_stablecoin_corridors.keys())


    date_range = [start_date - datetime.timedelta(days=i) for i in range(num_days -1, -1, -1)]
    date_range.sort() # Ensure dates are in ascending order

    for date in date_range:
        for inst in institutions:
            for coin in institution_stablecoin_corridors.get(inst, {}).keys():
                corridors_for_pair = institution_stablecoin_corridors[inst][coin]
                for corr in corridors_for_pair:
                    # Get base, trend, and volatility for the specific institution-stablecoin-corridor triplet
                    pos_config = base_positions_and_trends.get((inst, coin, corr), {"base": 0, "trend_per_day": 0, "volatility": 1000})
                    base = pos_config["base"]
                    trend_per_day = pos_config["trend_per_day"]
                    volatility = pos_config["volatility"]

                    # Calculate position based on base, trend, and days from the start of the 30-day period
                    days_index = (date - date_range[0]).days

                    trend_component = trend_per_day * days_index

                    # Add random fluctuation based on volatility
                    fluctuation = np.random.normal(0, volatility)

                    net_position = base + trend_component + fluctuation

                    data.append({
                        "Timestamp": date,
                        "Institution": inst,
                        "Corridor": corr,
                        "Stablecoin": coin,
                        "Net Position": round(net_position, 2)
                    })

    df = pd.DataFrame(data)
    df['Timestamp'] = pd.to_datetime(df['Timestamp']).dt.date # Keep only date for plotting historical

    return df

# Generate a new liquidity point, attempting to continue a recent trend
# Updated to pass volatility for more realistic new point generation
def generate_new_liquidity_point(last_position, historical_data_series, institution, corridor, stablecoin):
    """Generates a single new data point simulating real-time flow, projecting from recent trend."""
    timestamp = datetime.datetime.now()

    # Find the relevant volatility from the initial config for this triplet
    volatility = 1000 # Default volatility if not found
    for (inst, coin, corr), config in base_positions_and_trends.items():
        if inst == institution and coin == stablecoin and corr == corridor:
            volatility = config["volatility"]
            break

    # Calculate recent average daily change from historical data (e.g., last 7 days)
    recent_data = historical_data_series.tail(7)
    if len(recent_data) > 1:
        average_change = (recent_data.iloc[-1] - recent_data.iloc[0]) / (len(recent_data) - 1)
    else:
        average_change = 0 # No change if less than 2 points


    # Project position based on last position and average recent change, plus some noise
    # Use volatility from config for noise magnitude
    noise = np.random.normal(0, volatility * 1.5) # Add noise scaled by volatility
    new_position = last_position + average_change + noise

    # Optional: Keep new position within a broad plausible range
    new_position = max(new_position, -500000)
    new_position = min(new_position, 500000)


    return {
        "Timestamp": timestamp,
        "Institution": institution,
        "Corridor": corridor,
        "Stablecoin": stablecoin,
        "Net Position": round(new_position, 2)
    }


# Mock Compliance Alerts (Keep existing)
mock_compliance_alerts = [
    {"Alert ID": "ALERT001", "Timestamp": datetime.datetime.now() - datetime.timedelta(days=2), "Institution": "FinTech A", "Details": "High-value transaction (1M USDC) flagged for review in USD-MXN corridor.", "Status": "Pending"},
    {"Alert ID": "ALERT002", "Timestamp": datetime.datetime.now() - datetime.timedelta(days=1), "Institution": "PSP Alpha", "Details": "Multiple small transactions from new counterparty in EUR-NGN corridor.", "Status": "Reviewed"},
    {"Alert ID": "ALERT003", "Timestamp": datetime.datetime.now() - datetime.timedelta(hours=5), "Institution": "Bank B Mexico", "Details": "Unusual transaction pattern detected in EUR-USD corridor.", "Status": "Pending"},
]

# Dummy transaction volume data per corridor for the last 7 days
# Restricted to EUR-NGN and USD-MXN
dummy_volume_data = {
    "USD-MXN": [50, 60, 45, 70, 55, 80, 65],
    "EUR-NGN": [30, 35, 28, 40, 33, 45, 38],
    # Removed other corridors
}

# Dummy institution activity data for each corridor
# Restricted to EUR-NGN and USD-MXN
dummy_institution_activity = {
    "USD-MXN": {"FinTech A": 40, "PSP Alpha": 30, "Bank B Mexico": 20, "Others": 10},
    "EUR-NGN": {"FinTech Omega Nigeria": 50, "Bank B Mexico": 25, "PSP Alpha": 15, "Others": 10},
    # Removed other corridors
}

# Mock FX Rates (Ensured only USDC and EURC pairs are here)
FX_RATES = {
    ("EURC", "USDC"): 1.08,
    ("USDC", "EURC"): 1/1.08,
    ("USDC", "USDC"): 1.00,
    ("EURC", "EURC"): 1.00,
    # Removed SGDC and GBP rates
}