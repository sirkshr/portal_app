import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime

# -------------------
# Configurations
# -------------------
MASTER_SHEET_URL = "https://docs.google.com/spreadsheets/d/19HFwZWdBBBFzxmPJAe0R0GV1mPfUQm7oU8-JX7Tzae0/export?format=csv&id=19HFwZWdBBBFzxmPJAe0R0GV1mPfUQm7oU8-JX7Tzae0"
PROVIDER_CONTRACT_LINK = "https://your-google-drive-link-for-contracts"
PROVIDER_INVOICE_LINK = "https://your-google-drive-link-for-invoices"
PAYMENT_PORTAL_LINK = "https://your-payment-link.com"

# Dummy user database for login (for now)
users = {
    "provider1": {"password": "password123", "provider_name": "Provider One"},
    "provider2": {"password": "password456", "provider_name": "Provider Two"},
    "provider3": {"password": "password456", "provider_name": "Provider Three"}
}

# -------------------
# Helper Functions
# -------------------
def load_claims_data():
    df = pd.read_csv(MASTER_SHEET_URL)
    return df

def show_home():
    st.title("Welcome to Your Provider Portal")
    st.markdown("### Quick Access")
    st.button("View Claims Tracker", key="home_claims", on_click=lambda: st.session_state.update(page='Claims'))
    st.button("View Contract Details", key="home_contracts", on_click=lambda: st.session_state.update(page='Contracts'))
    st.button("View Invoices", key="home_invoices", on_click=lambda: st.session_state.update(page='Invoices'))
    st.button("Update Billing Info", key="home_billing", on_click=lambda: st.session_state.update(page='BillingInfo'))

def show_claims(provider_name):
    st.title("Claims Tracker")
    df = load_claims_data()
    provider_claims = df[df['Provider Name'] == provider_name]

    st.metric("Total Claims", len(provider_claims))
    st.metric("Total Billed", f"${provider_claims['Amount Billed'].sum():,.2f}")

    st.dataframe(provider_claims)

def show_contracts():
    st.title("Contract Management")
    st.markdown("### Contract Status")
    st.info("Your contract is currently Active. Renewal date: **12/31/2025**")
    st.markdown(f"[Download Your Current Contract]({PROVIDER_CONTRACT_LINK})")

def show_invoices():
    st.title("Invoice Center")
    st.markdown("### Past Invoices")
    st.markdown(f"[View Your Invoices]({PROVIDER_INVOICE_LINK})")

    st.markdown("### Make a Payment")
    st.markdown(f"[Go to Payment Portal]({PAYMENT_PORTAL_LINK})")

def show_billing_info_update():
    st.title("Update Billing Information")
    with st.form("billing_form"):
        billing_name = st.text_input("Billing Contact Name")
        billing_email = st.text_input("Billing Email Address")
        billing_phone = st.text_input("Billing Phone Number")
        billing_address = st.text_area("Billing Address")
        submitted = st.form_submit_button("Submit Update")

        if submitted:
            st.success("Your billing information has been submitted successfully! (for now this would be sent to admin)")

# -------------------
# App Logic
# -------------------

def main():
    st.set_page_config(page_title="Provider Portal", layout="wide")

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'page' not in st.session_state:
        st.session_state.page = 'Home'

    if not st.session_state.logged_in:
        st.title("Provider Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.button("Login")

        if login_button:
            user = users.get(username)
            if user and user['password'] == password:
                st.session_state.logged_in = True
                st.session_state.provider_name = user['provider_name']
                st.success("Login successful!")
            else:
                st.error("Invalid username or password")
    else:
        st.sidebar.title("Navigation")
        if st.sidebar.button("Home", key="sidebar_home"):
            st.session_state.page = 'Home'
        if st.sidebar.button("Claims Tracker", key="sidebar_claims"):
            st.session_state.page = 'Claims'
        if st.sidebar.button("Contracts", key="sidebar_contracts"):
            st.session_state.page = 'Contracts'
        if st.sidebar.button("Invoices", key="sidebar_invoices"):
            st.session_state.page = 'Invoices'
        if st.sidebar.button("Update Billing Info", key="sidebar_billing"):
            st.session_state.page = 'BillingInfo'
        if st.sidebar.button("Logout", key="sidebar_logout"):
            st.session_state.logged_in = False
            st.session_state.page = 'Home'

        # Page router
        if st.session_state.page == 'Home':
            show_home()
        elif st.session_state.page == 'Claims':
            show_claims(st.session_state.provider_name)
        elif st.session_state.page == 'Contracts':
            show_contracts()
        elif st.session_state.page == 'Invoices':
            show_invoices()
        elif st.session_state.page == 'BillingInfo':
            show_billing_info_update()

if __name__ == "__main__":
    main()
