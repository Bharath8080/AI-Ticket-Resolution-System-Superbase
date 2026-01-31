import streamlit as st
import uuid
import datetime
import random
from database import init_db, add_user, create_ticket, get_ticket_details
from ticket_processor import process_ticket
import threading

def generate_ticket_id():
    now = datetime.datetime.now()
    date_str = now.strftime("%Y%m%d%H%M")
    rand_suffix = random.randint(100, 999)
    return f"TRU-{date_str}-{rand_suffix}"

def run_agent_in_background(ticket_data):
    process_ticket(ticket_data)

# Header
st.markdown("<h1 style='text-align: center;'>🎫 Customer Support Portal</h1>", unsafe_allow_html=True)
st.markdown("---")

tab1, tab2 = st.tabs(["Raise a Ticket", "Track Status"])

with tab1:
    st.markdown("<h2 style='text-align: center;'>Submit your issue</h2>", unsafe_allow_html=True)
    
    # Get session data for auto-fill
    session_name = st.session_state.get("user_name", "")
    session_email = st.session_state.get("user_email", "")

    with st.form("ticket_form"):
        # Pre-filled fields
        name = st.text_input("Full Name", value=session_name, disabled=True)
        email = st.text_input("Email Address", value=session_email, disabled=True)
        
        # User inputs
        phone = st.text_input("Phone Number (Optional)")
        title = st.text_input("Issue Title", placeholder="e.g. Cannot play video")
        description = st.text_area("Detailed Description", placeholder="Please provide as much detail as possible...")
        
        submitted = st.form_submit_button("Submit Ticket")
        
        if submitted:
            if not title or not description:
                st.error("Please fill in Title and Description.")
            else:
                user_id = email
                add_user(user_id, name, email, phone)
                
                ticket_id = generate_ticket_id()
                create_ticket(ticket_id, user_id, title, description)
                
                st.success(f"Ticket Created Successfully! Your Ticket ID is: **{ticket_id}**")
                st.info("AI agents are analyzing your ticket. This may take a minute...")
                
                # Run AI analysis in background
                ticket_data = {
                    "ticket_id": ticket_id,
                    "title": title,
                    "description": description
                }
                thread = threading.Thread(target=run_agent_in_background, args=(ticket_data,))
                thread.start()

with tab2:
    st.markdown("<h2 style='text-align: center;'>Track Your Ticket</h2>", unsafe_allow_html=True)
    search_id = st.text_input("Enter Ticket ID (e.g. TRU-20260130...)")
    if st.button("Check Status", use_container_width=True):
        if search_id:
            ticket, logs = get_ticket_details(search_id)
            if not ticket.empty:
                t = ticket.iloc[0]
                
                # Ticket Header Card
                st.markdown(f"""
                    <div style="background-color: #1e1e1e; padding: 20px; border-radius: 10px; border-left: 5px solid #00b3ff; margin-bottom: 20px;">
                        <h2 style="margin: 0; color: #00b3ff;">Ticket: {t['title']}</h2>
                        <p style="color: #888;">ID: {t['ticket_id']} | Created: {t['created_at']}</p>
                    </div>
                """, unsafe_allow_html=True)

                # Status Metrics
                c1, c2, c3 = st.columns(3)
                
                status_color = "#28a745" if t['status'] == 'Resolved' else ("#ffc107" if t['status'] == 'Assigned' else "#00b3ff")
                c1.markdown(f"""
                    <div style="text-align: center; background: #262730; padding: 15px; border-radius: 10px;">
                        <p style="margin: 0; color: #888; font-size: 0.9em;">STATUS</p>
                        <h3 style="margin: 5px 0; color: {status_color};">{t['status']}</h3>
                    </div>
                """, unsafe_allow_html=True)
                
                sev_color = "#dc3545" if t['severity'] == 'P1' else ("#fd7e14" if t['severity'] == 'P2' else "#28a745")
                c2.markdown(f"""
                    <div style="text-align: center; background: #262730; padding: 15px; border-radius: 10px;">
                        <p style="margin: 0; color: #888; font-size: 0.9em;">SEVERITY</p>
                        <h3 style="margin: 5px 0; color: {sev_color};">{t['severity'] or 'Analyzing...'}</h3>
                    </div>
                """, unsafe_allow_html=True)
                
                c3.markdown(f"""
                    <div style="text-align: center; background: #262730; padding: 15px; border-radius: 10px;">
                        <p style="margin: 0; color: #888; font-size: 0.9em;">PRIORITY</p>
                        <h3 style="margin: 5px 0; color: #00b3ff;">{t['priority'] or 'Analyzing...'}</h3>
                    </div>
                """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # Details Section
                with st.container(border=True):
                    st.markdown("### 📝 Details")
                    st.write(f"**Description:** {t['description']}")
                    st.write(f"**Category:** {t['category'] or 'Analyzing...'}")
                    
                    if t['status'] == 'Assigned':
                        st.info(f"**Assignment Context:** {t['assignment_reason']}")
                    elif t['status'] == 'Resolved':
                        st.success(f"**Resolution Notes:** {t['resolution_notes']}")
                        if st.button("Unsatisfied? Re-open Ticket"):
                            from database import log_action, get_supabase_client
                            client = get_supabase_client()
                            client.table("tickets").update({"status": "Open"}).eq("ticket_id", search_id).execute()
                            log_action(search_id, "Ticket Re-opened", "User re-opened the ticket.")
                            st.warning("Ticket Re-opened and sent back to queue.")
                            st.rerun()

                st.markdown("<br>", unsafe_allow_html=True)

                # Activity Timeline Section
                st.markdown("### 🕒 Activity Timeline")
                for _, log in logs.iterrows():
                    with st.container(border=True):
                        ts = str(log['timestamp']).split('.')[0]
                        st.markdown(f"**{log['action']}**")
                        st.caption(ts)
                        st.write(log['details'])
            else:
                st.error("Ticket ID not found.")
        else:
            st.warning("Please enter a Ticket ID.")
