import os
# MANDATORY: Disables CrewAI telemetry to prevent "signal only works in main thread" errors in Streamlit
os.environ["CREWAI_TELEMETRY_OPTOUT"] = "true"

import streamlit as st
from dotenv import load_dotenv
from database import init_db

load_dotenv()

# Initialize Database at the very beginning
init_db()

# Page configuration
st.set_page_config(
    page_title="Trugen AI Support",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Force hide sidebar when not logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {display: none;}
            [data-testid="stSidebar"] {display: none;}
            .st-emotion-cache-1wf8p8v {display: none;} /* Hide the sidebar collapse button */
            button[kind="header"] {display: none;} /* Hide the hamburger menu */
        </style>
        """,
        unsafe_allow_html=True,
    )

# Session state initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_email" not in st.session_state:
    st.session_state.user_email = ""

def logout():
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.user_name = ""
    st.session_state.user_email = ""
    st.rerun()

# --- LOGIN SCREEN ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #00b3ff;'>Trugen AI Support</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>Welcome! Please log in to continue.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.subheader("👤 User Portal")
            st.write("Raise and track your support tickets.")
            user_name = st.text_input("Full Name", placeholder="John Doe")
            user_email = st.text_input("Email Address", placeholder="john@example.com")
            if st.button("Enter Portal", use_container_width=True):
                if user_name and user_email:
                    st.session_state.logged_in = True
                    st.session_state.role = "User"
                    st.session_state.user_name = user_name
                    st.session_state.user_email = user_email
                    st.rerun()
                else:
                    st.error("Please provide both name and email.")

    with col2:
        with st.container(border=True):
            st.subheader("🛡️ Admin Dashboard")
            st.write("Manage tickets and view analytics.")
            admin_password = st.text_input("Admin Password", type="password")
            if st.button("Login as Admin", use_container_width=True):
                expected_password = os.getenv("ADMIN_PASSWORD", "admin123")
                if admin_password == expected_password:
                    st.session_state.logged_in = True
                    st.session_state.role = "Admin"
                    st.rerun()
                else:
                    st.error("Invalid Admin Password")
    st.stop()

# --- AFTER LOGIN ---
# Define the navigation based on role
if st.session_state.role == "User":
    pages = [st.Page("portals/user_portal.py", title="Customer Portal", icon="🎫")]
else:
    pages = [st.Page("portals/admin_dashboard.py", title="Admin Dashboard", icon="🛡️")]

# Sidebar info
with st.sidebar:
    st.title("Trugen AI")
    if st.session_state.role == "User":
        st.write(f"Logged in as: **{st.session_state.user_name}**")
    else:
        st.write("Logged in as: **Support Admin**")
    
    if st.button("🚪 Logout", use_container_width=True):
        logout()

# Navigation setup
pg = st.navigation(pages, position="hidden")
pg.run()
