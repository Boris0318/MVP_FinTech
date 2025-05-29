import streamlit as st
import pandas as pd
import time
import uuid 
from src.utils import calculate_fee, create_ledger_entry # Assuming .utils for relative import
from src.config_base import FX_RATES # Assuming .config_base for relative import

def render_payments_tab():
    """Renders the Payments tab UI and handles payment submission."""
    st.header("Cross-Border Payment Simulation")
    st.write("Experience instant, low-cost settlements.")

    with st.form("payment_form"):
        col1, col2 = st.columns(2)
        with col1:
            sending_institution = st.text_input("Sending Institution", placeholder="e.g., FinTech A", help="Enter the name of the sending financial institution.")
            # Restricted corridors
            corridor = st.selectbox("Corridor", ["USD-MXN", "EUR-NGN"], help="Select the payment corridor.")
            amount_to_send = st.number_input("Amount to Send", min_value=100, value=5000, step=100, help="Enter the amount to send (minimum 100).")
            # Restricted stablecoins
            sending_stablecoin = st.selectbox("Sending Stablecoin", ["USDC", "EURC"], help="Select the stablecoin to send.")
        with col2:
            receiving_institution = st.text_input("Receiving Institution", placeholder="e.g., Bank B Mexico", help="Enter the name of the receiving financial institution.")
            # Default receiving stablecoin based on corridor and sending, allow change
            default_receiving_stablecoin = sending_stablecoin # Default to sending
            if corridor == "USD-MXN":
                default_receiving_stablecoin = "USDC"
            elif corridor == "EUR-NGN":
                 default_receiving_stablecoin = "EURC"
            # Restricted stablecoins
            receiving_stablecoin = st.selectbox("Receiving Stablecoin", ["USDC", "EURC"], index=["USDC", "EURC"].index(default_receiving_stablecoin) if default_receiving_stablecoin in ["USDC", "EURC"] else 0, help="Select the stablecoin the recipient will receive.")

            transaction_priority = st.radio("Transaction Priority", ["Standard", "High Priority"], help="Standard has lower fee, High Priority adds 50% to fee.")

        submit_button = st.form_submit_button("Submit Payment")

        # Input Validation
        errors = []
        if not sending_institution:
            errors.append("Sending Institution name is required.")
        # Basic regex for institution names: letters, numbers, spaces, hyphens allowed.
        # if sending_institution and not re.match("^[a-zA-Z0-9 -]+$", sending_institution):
        #     errors.append("Sending Institution name contains invalid characters.") # Need to import 're'
        if not receiving_institution:
             errors.append("Receiving Institution name is required.")
        # if receiving_institution and not re.match("^[a-zA-Z0-9 -]+$", receiving_institution):
        #      errors.append("Receiving Institution name contains invalid characters.") # Need to import 're'
        if amount_to_send < 100:
            errors.append("Amount to Send must be at least 100.")
        # Updated stablecoin check
        if sending_stablecoin not in ["USDC", "EURC"]:
             errors.append("Invalid Sending Stablecoin selected.")
        if receiving_stablecoin not in ["USDC", "EURC"]:
             errors.append("Invalid Receiving Stablecoin selected.")

        # Check if FX rate exists for the selected stablecoin pair
        if (sending_stablecoin, receiving_stablecoin) not in FX_RATES:
             errors.append(f"No FX rate available for {sending_stablecoin} to {receiving_stablecoin}.")


        if submit_button:
            if errors:
                for error in errors:
                    st.error(error)
            else:
                # Simulate processing
                with st.spinner("Processing payment on StableNet Ledger..."):
                    # Simulate network latency
                    time.sleep(2)

                    # Calculate fee
                    fee = calculate_fee(amount_to_send, transaction_priority)
                    st.success(f"Payment settled instantly! Transaction ID: {uuid.uuid4().hex[:8].upper()}")

                    # Show fee comparison - Fee is calculated on amount_sent, but displayed in Receiving Stablecoin's equivalent value
                    # Let's calculate fee in sending stablecoin for simplicity in calculation,
                    # but the comparison is against a USD value.
                    # We'll display the fee in the sending stablecoin units.
                    st.metric(label="StableNet Fee", value=f"{fee:.4f} {sending_stablecoin}", delta=f"vs. CBS Fee: ~{amount_to_send*0.01}-{amount_to_send*0.05} USD (estimated)", delta_color="inverse")


                    # Add transaction to ledger
                    new_transaction = create_ledger_entry(
                        sending_institution=sending_institution,
                        receiving_institution=receiving_institution,
                        corridor=corridor,
                        amount_sent=amount_to_send,
                        sending_stablecoin=sending_stablecoin,
                        receiving_stablecoin=receiving_stablecoin,
                        priority=transaction_priority,
                        fee=fee # Fee recorded in sending stablecoin units
                    )
                    # Convert to DataFrame and concatenate, handling potential empty initial state
                    new_transaction_df = pd.DataFrame([new_transaction])
                    if 'transactions' in st.session_state:
                        st.session_state['transactions'] = pd.concat([st.session_state['transactions'], new_transaction_df], ignore_index=True)
                    else:
                         st.session_state['transactions'] = new_transaction_df


                st.balloons()

                st.markdown("""
                ---
                **Comparison vs. Traditional Correspondent Banking System (CBS):**

                | Feature      | StableNet Ledger          | Traditional CBS          |
                |--------------|---------------------------|--------------------------|
                | Speed        | Instant                   | 2-5 Days                 |
                | Cost         | Very Low (e.g., 0.01%)    | High (e.g., 30-50 USD)   |
                | Transparency | Full, Immutable Ledger    | Limited Visibility       |
                """) 