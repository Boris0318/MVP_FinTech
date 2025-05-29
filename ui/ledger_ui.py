import streamlit as st
import pandas as pd

def render_ledger_tab():
    """Renders the Ledger tab UI and displays transactions."""
    st.header("Immutable Transaction Ledger")
    st.write("Every payment is logged for transparency and compliance.")

    if 'transactions' in st.session_state and not st.session_state['transactions'].empty:
        # Filter Widget
        all_institutions = sorted(list(set(st.session_state['transactions']['Sending Institution'].tolist() + st.session_state['transactions']['Receiving Institution'].tolist())))
        selected_institutions = st.multiselect("Filter by Institution", all_institutions, default=[], placeholder="Select institutions...")

        # Restricted corridors
        all_corridors = ["USD-MXN", "EUR-NGN"]
        selected_corridors = st.multiselect("Filter by Corridor", all_corridors, default=[], placeholder="Select corridors...")


        filtered_df = st.session_state['transactions']
        if selected_institutions:
            filtered_df = filtered_df[
                filtered_df['Sending Institution'].isin(selected_institutions) |
                filtered_df['Receiving Institution'].isin(selected_institutions)
            ]
        if selected_corridors:
            filtered_df = filtered_df[filtered_df['Corridor'].isin(selected_corridors)]


        st.dataframe(filtered_df, use_container_width=True)

        # Summary Metrics
        total_transactions = len(filtered_df)
        # Calculate total fees per stablecoin in the filtered data
        if not filtered_df.empty:
             fee_summary = filtered_df.groupby('Sending Stablecoin')['Fee'].sum().reset_index() # Fee is in Sending Stablecoin
             fee_text_parts = [f"{row['Fee']:.4f} {row['Sending Stablecoin']}" for index, row in fee_summary.iterrows()]
             fee_text = ", ".join(fee_text_parts)
        else:
             fee_text = "0.0000 USD"


        col_metrics1, col_metrics2 = st.columns(2)
        with col_metrics1:
            st.metric("Total Transactions Shown", total_transactions)
        with col_metrics2:
             st.metric("Total Fees Collected (Shown)", fee_text)


        # CSV Export
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Export Ledger to CSV",
            data=csv,
            file_name='stablenet_ledger.csv',
            mime='text/csv',
        )
    else:
        st.info("No transactions recorded yet. Submit a payment to see it appear here.") 