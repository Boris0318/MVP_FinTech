# StableNet Ledger MVP Streamlit Application

## Project Objective

This project is a Minimum Viable Product (MVP) Streamlit application for the StableNet Ledger, designed for cross-border payments. The MVP simulates core functionalities including instantaneous settlements using regulated stablecoins (USDC, EURC) on a permissioned DLT network, a transparent transaction ledger, AI-powered liquidity forecasting and management, and simulated compliance checks.

The goal of this MVP is to provide a visually, interactive, and intuitive demonstration for investors and stakeholders, highlighting the platform's potential to disrupt the traditional correspondent banking system (CBS) by emphasizing speed, cost-efficiency, transparency, liquidity optimization, and regulatory compliance.

**Note:** All core functionalities in this MVP are simulated and do not connect to real-world DLT networks, stablecoin protocols, or external data feeds.

## Key Simulated Features

*   **User Interface (Main Dashboard):** A professional, modern dashboard using Streamlit's layout features (`st.columns`, `st.container`, `st.tabs`) with a sticky sidebar.
*   **Payments Simulation:** Demonstrate instant, low-cost cross-border settlements between simulated institutions using USDC and EURC in USD-MXN and EUR-NGN corridors.
*   **Immutable Transaction Ledger:** A transparent log of all simulated transactions, filterable by institution and corridor.
*   **AI-Powered Liquidity Forecasting & Management:** Simulated real-time liquidity forecasting using historical data, displaying two simulated forecast paths (EMA-like and ARIMA-like) and providing proactive recommendations based on projected net positions.
*   **Compliance Analytics:** Simulated views of transaction volume and compliance alerts within selected corridors.

## Setup and Running the Project

To set up and run this Streamlit application locally, follow these steps:

1.  **Clone the Repository:**

    ```bash
    # Assuming your code is in a repository, replace with actual clone command
    # git clone <repository_url>
    # cd <repository_directory>
    ```

2.  **Navigate to the Project Directory:**

    ```bash
    cd path/to/your/project/MVP
    ```

3.  **Create a Virtual Environment (Recommended):**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

4.  **Install Dependencies:**

    Make sure you have the necessary libraries installed. You can use the following command:

    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the Streamlit Application Locally:**

    ```bash
    streamlit run app.py
    ```
6. If you are too lazy for all this setup, try the available public online application I deployed using this code on: https://mvpfintech-boris.streamlit.app/

    This will start the application, and it should open in your web browser.
   **Note:** The app might be on a sleep state, to wake it up press on the "Yes, get this app back up!" button to test the app. This will take around a minute

## Project Structure

```plaintext
.
├── app.py #  Main executable for MVP application
├── src/
│   ├── config_base.py # Contains configuration data and dummy data generation
│   ├── data_manager.py # Manages session state and data operations
│   ├── utils.py # Provides helper functions used across the application
├── ui/
│   ├── payments_ui.py #  Handles the Payments tab UI and logic
│   ├── ledger_ui.py # Manages the Ledger tab UI and logic
│   ├── compliance_ui.py # Implements the Compliance Analytics tab UI and logic
│   ├── liquidity_ui.py # Contains the Liquidity Forecast tab UI and logic
├── requirements.txt  # txt file containing all necessary software dependencies to run the project
└── README.md  
```

## Demo Walkthrough

The application is designed for a guided demonstration. Navigate through the tabs to showcase:

1.  **Payments:** Simulate a cross-border transfer to demonstrate speed and low cost.
2.  **Ledger:** Show the transparency of the immutable transaction log.
3.  **Liquidity Forecast:** Select an institution, stablecoin, and corridor to generate simulated forecasts and explain the AI recommendations.
4.  **Compliance Analytics:** Display simulated transaction volume and compliance alerts.

Refer to the demo script for a timed narrative to follow during a presentation.

## Target Audience

This MVP is primarily aimed at Investors, FinTech Executives, and Payment Service Providers (PSPs) to help them understand the value proposition and potential of the StableNet Ledger.

## License

No required licenses :)

## Contact

715195be@eur.nl

