import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from config_base import mock_compliance_alerts, dummy_volume_data, dummy_institution_activity

def render_compliance_tab():
    """Renders the Compliance Analytics tab UI and handles analysis."""
    st.header("Simulated Compliance Analytics")
    st.write("Ensure regulatory alignment with built-in checks and reporting.")

    with st.form("compliance_form"):
        # Restricted corridors
        compliance_corridor = st.selectbox("Select Corridor", ["USD-MXN", "EUR-NGN"], help="Select the corridor for analysis.")
        analysis_type = st.radio("Analysis Type", ["Transaction Volume", "Compliance Alerts", "Institution Activity"], help="Choose the type of compliance analysis.")

        run_analysis_button = st.form_submit_button("Run Analysis")

    if run_analysis_button:
        if analysis_type == "Transaction Volume":
            st.subheader(f"Daily Transaction Volume for {compliance_corridor}")
            volume_data = dummy_volume_data.get(compliance_corridor, [0] * 7)
            days = list(range(1, len(volume_data) + 1))
            fig = go.Figure(data=go.Bar(x=[f"Day {d}" for d in days], y=volume_data))
            fig.update_layout(title=f"Simulated Daily Transaction Volume - {compliance_corridor}", xaxis_title="Day", yaxis_title="Number of Transactions")
            st.plotly_chart(fig, use_container_width=True)
            st.caption("Visualizing transaction flow to identify patterns.")

        elif analysis_type == "Compliance Alerts":
            st.subheader("Simulated Compliance Alerts")
            alerts_df = pd.DataFrame(mock_compliance_alerts)
            # Filter alerts relevant to selected corridor (simplified for demo)
            if compliance_corridor == "USD-MXN":
                filtered_alerts = alerts_df[alerts_df['Details'].str.contains("USD-MXN", na=False)]
            elif compliance_corridor == "EUR-NGN":
                filtered_alerts = alerts_df[alerts_df['Details'].str.contains("EUR-NGN", na=False)]
            else:
                filtered_alerts = pd.DataFrame() # Empty if no alerts for corridor

            if not filtered_alerts.empty:
                st.dataframe(filtered_alerts, use_container_width=True)
            else:
                st.info(f"No simulated compliance alerts for {compliance_corridor} at this time.")
            st.caption("Monitoring transactions for suspicious activity.")

        elif analysis_type == "Institution Activity":
            st.subheader(f"Institution Transaction Share in {compliance_corridor}")
            activity_data = dummy_institution_activity.get(compliance_corridor, {})
            if activity_data:
                labels = list(activity_data.keys())
                values = list(activity_data.values())
                fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
                fig.update_layout(title=f"Simulated Institution Transaction Share - {compliance_corridor}")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(f"No simulated institution activity data for {compliance_corridor}.")
            st.caption("Analyzing participant activity within corridors.")

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("All transactions undergo simulated AML/CFT checks for regulatory compliance.", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.caption("StableNet ensures compliance with global regulations, building trust.") 