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
    layout="centered"
)

# Title and description
st.markdown(
    """
    <h1 style='text-align:center'>
        <span style='color:#00b3ff;'>AI Ticket Resolution System</span>
    </h1>
    """,
    unsafe_allow_html=True
)

# Define pages
pages_dict = {
    "🎫 User Portal": st.Page("pages/user_portal.py", title="User Portal", default=True),
    "🛡️ Admin Dashboard": st.Page("pages/admin_dashboard.py", title="Admin Dashboard"),
}

# Define pages with icons
pages_config = {
    "User Portal": {"page": pages_dict["🎫 User Portal"], "icon": ":material/support_agent:"},
    "Admin Dashboard": {"page": pages_dict["🛡️ Admin Dashboard"], "icon": ":material/admin_panel_settings:"},
}

# Navigation setup
pg = st.navigation(list(pages_dict.values()), position="hidden")

# Sidebar navigation or top navigation
st.markdown("<br>", unsafe_allow_html=True)
cols = st.columns([1, 2, 1])
with cols[1]:
    selected_page_label = st.pills(
        "Navigation",
        options=list(pages_config.keys()),
        format_func=lambda x: pages_config[x]["icon"] + " " + x,
        selection_mode="single",
        label_visibility="collapsed",
        default="User Portal" if pg.title == "User Portal" else "Admin Dashboard"
    )

# Routing logic
if selected_page_label:
    target_page = pages_config[selected_page_label]["page"]
    if pg.title != target_page.title:
        st.switch_page(target_page)

pg.run()
