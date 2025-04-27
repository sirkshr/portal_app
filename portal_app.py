import streamlit as st
import pandas as pd
import requests

# Set page config
st.set_page_config(page_title="Provider Portal", layout="wide")

# Apply background styling
st.markdown("""
    <style>
    .block-container {
        background-color: #f7f7f7;
        padding-top: 0px;
        padding-bottom: 0px;
    }
    header {
        background-color: #6a0dad;
        color: white;
        padding: 10px;
        text-align: center;
        font-size: 26px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# User database simulation
users = {
    "admin": {"password": "adminpass", "role": "admin"},
    "provider1": {"password": "providerpass", "role": "provider", "provider_name": "Sunrise Health"},
    "provider2": {"password": "providerpass", "role": "provider", "provider_name": "Hope Wellness"},
}

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None
if "provider_name" not in st.session_state:
    st.session_state.provider_name = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

# Placeholder for Supabase integration
def connect_supabase():
    # Add your Supabase project URL and API key here later
    pass

def fetch_user_data():
    # Pull user-specific data from Supabase later
    pass

def store_claim_data(data):
    # Push claim data to Supabase later
    pass

# Placeholder for Make.com webhook
def trigger_make_webhook(event_type, payload):
    try:
        webhook_url = "https://your-make-webhook-url.com"
        requests.post(webhook_url, json={"event": event_type, "data": payload})
    except:
        st.warning("Webhook trigger failed (placeholder)")

# Placeholder for Stripe payment (future ACH, CC integration)
def setup_stripe_payment_portal():
    # Future Stripe integration will go here
    st.info("Stripe payment setup will be configured here.")
# Top navigation bar
def top_navigation():
    st.markdown("<header>Provider Portal</header>", unsafe_allow_html=True)

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        if st.button("Home"):
            st.session_state.current_page = "Home"
    with col2:
        if st.button("Claims Tracker"):
            st.session_state.current_page = "Claims Tracker"
    with col3:
        if st.button("Contracts"):
            st.session_state.current_page = "Contracts"
    with col4:
        if st.button("Invoices"):
            st.session_state.current_page = "Invoices"
    with col5:
        if st.button("Billing Info"):
            st.session_state.current_page = "Billing Info"
    with col6:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.role = None
            st.session_state.provider_name = None
            st.session_state.current_page = "Home"

# Home Page
def show_home():
    st.title("Welcome to Your Provider Portal")
    st.subheader("Quick Access Dashboard")

# Claims Tracker Page
def show_claims():
    st.title("Claims Tracker")
    try:
        sheet_url = "https://docs.google.com/spreadsheets/d/19HFwZWdBBBFzxmPJAe0R0GV1mPfUQm7oU8-JX7Tzae0/export?format=csv"
        claims_df = pd.read_csv(sheet_url)

        if st.session_state.role == "provider":
            claims_df = claims_df[claims_df["Provider"] == st.session_state.provider_name]

        st.dataframe(claims_df)
    except Exception as e:
        st.error(f"Error loading claims data: {e}")
# Contracts Page
def show_contracts():
    st.title("Contracts")
    st.info("Contracts will be displayed here. (Future upload/download feature placeholder)")

# Invoices Page
def show_invoices():
    st.title("Invoices")
    st.info("Invoices will be listed here. (Future billing system and downloadable invoices placeholder)")

# Billing Info Page
def show_billing_info():
    st.title("Billing Information")
    st.info("Billing details and Stripe integration will be managed here (ACH and Card setup future).")
    setup_stripe_payment_portal()

# Main Application Controller
def main():
    if st.session_state.logged_in:
        top_navigation()

        if st.session_state.current_page == "Home":
            show_home()
        elif st.session_state.current_page == "Claims Tracker":
            show_claims()
        elif st.session_state.current_page == "Contracts":
            show_contracts()
        elif st.session_state.current_page == "Invoices":
            show_invoices()
        elif st.session_state.current_page == "Billing Info":
            show_billing_info()
    else:
        login()

# Login Screen
def login():
    st.markdown("<header>Provider Portal Login</header>", unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login")

    if login_btn:
        if username in users and users[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.role = users[username]["role"]
            if users[username]["role"] == "provider":
                st.session_state.provider_name = users[username]["provider_name"]
            st.session_state.current_page = "Home"
        else:
            st.error("Invalid username or password")

if __name__ == "__main__":
    main()
