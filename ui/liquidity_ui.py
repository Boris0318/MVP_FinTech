import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import datetime
from src.config_base import institution_stablecoin_corridors
from src.data_manager import refresh_liquidity_data
import numpy as np
@st.cache_data
def calculate_simulated_forecast_paths(data_series, forecast_horizon=7, num_paths=3):
    """
    Calculates simulated forecast paths based on recent trend and historical volatility.
    This is a simulation, not a true ARIMA model.
    """
    if data_series.empty or len(data_series) < 2:
        return [pd.Series()] * num_paths

    recent_data = data_series.sort_index().tail(30)

    if len(recent_data) < 2:
        last_value = recent_data.iloc[-1] if not recent_data.empty else 0
        forecast_values = [last_value] * forecast_horizon
        last_historical_date = recent_data.index.max()
        if not isinstance(last_historical_date, datetime.datetime) and not isinstance(last_historical_date, pd.Timestamp):
            last_historical_date = datetime.datetime.combine(last_historical_date, datetime.datetime.min.time())
        forecast_dates = pd.date_range(start=last_historical_date + pd.Timedelta(days=1), periods=forecast_horizon, freq='D')
        flat_series = pd.Series(forecast_values, index=forecast_dates)
        return [flat_series] * num_paths

    x = np.arange(len(recent_data))
    y = recent_data.values
    try:
        m, c = np.polyfit(x, y, 1)
    except np.linalg.LinAlgError:
        m, c = 0, y[-1]

    daily_changes = recent_data.diff().dropna()
    volatility = daily_changes.std() if not daily_changes.empty else 1000

    last_historical_index = len(recent_data) - 1
    primary_forecast_values = [m * (last_historical_index + 1 + i) + c for i in range(forecast_horizon)]

    last_historical_date = recent_data.index.max()
    if not isinstance(last_historical_date, datetime.datetime) and not isinstance(last_historical_date, pd.Timestamp):
        last_historical_date = datetime.datetime.combine(last_historical_date, datetime.datetime.min.time())
    forecast_dates = pd.date_range(start=last_historical_date + pd.Timedelta(days=1), periods=forecast_horizon, freq='D')

    forecast_paths = []
    for _ in range(num_paths):
        path_values = []
        current_value = primary_forecast_values[0]
        path_values.append(current_value)

        for i in range(1, forecast_horizon):
            step_noise = np.random.normal(0, volatility)
            current_value = path_values[-1] + m + step_noise
            path_values.append(current_value)

        forecast_paths.append(pd.Series(path_values, index=forecast_dates))

    return forecast_paths

def render_liquidity_tab():
    """Renders the Liquidity Forecast tab UI and handles forecasting."""
    st.header("AI-Powered Liquidity Forecasting & Management")
    st.write("Simulated real-time insights to optimize treasury efficiency.")

    with st.form("liquidity_form"):
        # Institutions available based on the mapping
        liquidity_institutions_available = list(institution_stablecoin_corridors.keys())
        liquidity_institution = st.selectbox("Institution", liquidity_institutions_available, help="Select the institution to forecast liquidity for.")

        # Offer all relevant stablecoins (USDC, EURC) as options
        available_stablecoins = ["USDC", "EURC"]
        current_stablecoin_index = 0
        if 'liquidity_stablecoin_state' in st.session_state and st.session_state['liquidity_stablecoin_state'] in available_stablecoins:
            current_stablecoin_index = available_stablecoins.index(st.session_state['liquidity_stablecoin_state'])
        liquidity_stablecoin = st.selectbox("Stablecoin", available_stablecoins, index=current_stablecoin_index, help="Select the stablecoin to forecast.", key='liquidity_stablecoin_state')

        # Offer all relevant corridors
        available_corridors = ["USD-MXN", "EUR-NGN"]
        current_corridor_index = 0
        if 'liquidity_corridor_state' in st.session_state and st.session_state['liquidity_corridor_state'] in available_corridors:
            current_corridor_index = available_corridors.index(st.session_state['liquidity_corridor_state'])
        liquidity_corridor = st.selectbox("Corridor", available_corridors, index=current_corridor_index, help="Select the relevant corridor.", key='liquidity_corridor_state')

        forecast_horizon = st.slider("Forecast Horizon (Days)", 3, 14, 7, help="Select the number of days to forecast liquidity.")
        simulate_stress = st.checkbox("Simulate Stress Scenario (20% increased outflows)", help="Toggle to see impact of a stress scenario on liquidity.")

        col_liq_buttons1, col_liq_buttons2 = st.columns(2)
        with col_liq_buttons1:
            generate_forecast_button = st.form_submit_button("Generate Forecast")
        with col_liq_buttons2:
            refresh_data_button = st.form_submit_button("Refresh Data")

    # Handle Data Refresh
    if refresh_data_button:
        refresh_liquidity_data(liquidity_institution, liquidity_corridor, liquidity_stablecoin)

    # Generate and Display Forecast
    if generate_forecast_button or refresh_data_button:
        if liquidity_institution and liquidity_stablecoin and liquidity_corridor:
            filtered_data_for_plot = st.session_state['liquidity_data'][
                (st.session_state['liquidity_data']['Institution'] == liquidity_institution) &
                (st.session_state['liquidity_data']['Corridor'] == liquidity_corridor) &
                (st.session_state['liquidity_data']['Stablecoin'] == liquidity_stablecoin)
            ].sort_values(by='Timestamp').set_index('Timestamp')['Net Position']

            st.session_state['last_filtered_liquidity_data_for_plot'] = filtered_data_for_plot
            st.session_state['last_liq_institution'] = liquidity_institution
            st.session_state['last_liq_corridor'] = liquidity_corridor
            st.session_state['last_liq_stablecoin'] = liquidity_stablecoin

            if not filtered_data_for_plot.empty:
                with st.spinner("Generating AI insights..."):
                    forecast_paths = calculate_simulated_forecast_paths(
                        filtered_data_for_plot,
                        forecast_horizon=forecast_horizon,
                        num_paths=2
                    )

                    forecast_paths_adjusted = []
                    path_names = ['Simulated EMA', 'Simulated ARIMA']

                    for i, path_series in enumerate(forecast_paths):
                        path_values_adjusted = list(path_series.values)
                        if simulate_stress:
                            path_values_adjusted = [d - (abs(d) * 0.20) for d in path_values_adjusted]
                        forecast_paths_adjusted.append({
                            'name': path_names[i] if i < len(path_names) else f'Simulated Forecast Path {i+1}',
                            'series': pd.Series(path_values_adjusted, index=path_series.index)
                        })

                    st.session_state['last_forecast_paths_adjusted'] = forecast_paths_adjusted

                    # Create Plotly chart
                    fig = go.Figure()

                    historical_data_view = filtered_data_for_plot.tail(30)

                    fig.add_trace(go.Scatter(
                        x=historical_data_view.index,
                        y=historical_data_view.values,
                        mode='lines+markers',
                        name='Historical Data',
                        line=dict(color='blue'),
                        marker=dict(size=5)
                    ))

                    for path_info in forecast_paths_adjusted:
                        fig.add_trace(go.Scatter(
                            x=path_info['series'].index,
                            y=path_info['series'].values,
                            mode='lines',
                            name=path_info['name'],
                            line=dict(color='red' if 'EMA' in path_info['name'] else 'green',
                                    dash='dash' if 'EMA' in path_info['name'] else 'dot'),
                            opacity=1.0 if 'EMA' in path_info['name'] else 0.8
                        ))

                    fig.add_hline(y=-10000, line_dash="dash", line_color="darkred", annotation_text="Shortfall Threshold (-10k)", annotation_position="bottom right")
                    fig.add_hline(y=50000, line_dash="dash", line_color="darkgreen", annotation_text="Surplus Threshold (50k)", annotation_position="bottom right")

                    fig.update_layout(
                        title=f"Liquidity Forecast - {liquidity_institution} in {liquidity_corridor} ({liquidity_stablecoin})",
                        xaxis_title="Date",
                        yaxis_title=f"Net Position ({liquidity_stablecoin})",
                        hovermode="x unified",
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                    )

                    st.plotly_chart(fig, use_container_width=True)

                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.subheader("AI Recommendations")

                    if forecast_paths_adjusted:
                        path_series_list = [path_info['series'] for path_info in forecast_paths_adjusted]
                        if path_series_list:
                            combined_paths_df = pd.concat(path_series_list, axis=1)
                            average_forecast_series = combined_paths_df.mean(axis=1)

                            recommendations = []
                            for i in range(forecast_horizon):
                                forecasted_balance = average_forecast_series.iloc[i]
                                date = average_forecast_series.index[i].strftime('%Y-%m-%d')

                                if forecasted_balance < -10000:
                                    recommendations.append(f"Projected average shortfall of {abs(forecasted_balance):,.0f} for {liquidity_institution} in {liquidity_corridor} ({liquidity_stablecoin}) on **{date}** (Day {i+1}). **Recommendation:** Source {liquidity_stablecoin} or adjust flows.")
                                elif forecasted_balance > 50000:
                                    recommendations.append(f"Projected average surplus of {forecasted_balance:,.0f} for {liquidity_institution} in {liquidity_corridor} ({liquidity_stablecoin}) on **{date}** (Day {i+1}). **Recommendation:** Offer short-term lending on StableNet.")

                            if recommendations:
                                for rec in recommendations:
                                    st.warning(rec)
                            else:
                                st.info(f"No significant liquidity concerns projected on average for {liquidity_institution} in {liquidity_corridor} ({liquidity_stablecoin}) over the next {forecast_horizon} days.")
                        else:
                            st.info("Could not generate average forecast for recommendations.")
                    else:
                        st.info("Generate a forecast to see recommendations.")

                    st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("Select an Institution, Stablecoin, and Corridor with available historical data to generate a forecast.")
        else:
            st.info("Please select Institution, Stablecoin, and Corridor to generate a forecast.") 