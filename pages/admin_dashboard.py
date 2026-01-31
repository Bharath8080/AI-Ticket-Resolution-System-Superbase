import streamlit as st
import pandas as pd
from database import get_all_tickets, get_ticket_details, resolve_ticket, get_managers
import plotly.express as px

# Header
st.markdown("<h1 style='text-align: center;'>🛡️ Support Admin Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

# Dashboard Content (Authentication is handled globally in app.py)
# Sidebar Filters
st.sidebar.header("Filters")
tickets_df = get_all_tickets()

if tickets_df.empty:
    st.info("No tickets found in the system.")
else:
    status_filter = st.sidebar.multiselect("Status", options=tickets_df['status'].unique(), default=tickets_df['status'].unique())
    # Filter out None from severity options
    severity_options = [s for s in tickets_df['severity'].unique().tolist() if s is not None]
    severity_filter = st.sidebar.multiselect("Severity", options=severity_options, default=severity_options)
    
    filtered_df = tickets_df[
        (tickets_df['status'].isin(status_filter)) & 
        (tickets_df['severity'].isin(severity_filter + [None]))
    ]

    # Top Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Tickets", len(tickets_df))
    m2.metric("Open Tickets", len(tickets_df[tickets_df['status'] == 'Open']))
    m3.metric("Resolved Tickets", len(tickets_df[tickets_df['status'] == 'Resolved']))
    m4.metric("Managers Active", len(get_managers()))

    st.markdown("### Ticket Overview")
    st.dataframe(filtered_df[['ticket_id', 'title', 'status', 'severity', 'priority', 'manager_name', 'created_at']], width='stretch')

    st.markdown("---")
    st.subheader("Ticket Action Center")
    ticket_to_action = st.selectbox("Select Ticket to Manage", options=filtered_df['ticket_id'].tolist())
    
    if ticket_to_action:
        ticket, logs = get_ticket_details(ticket_to_action)
        t = ticket.iloc[0]
        
        # Management Section
        with st.container(border=True):
            st.write(f"**Title:** {t['title']}")
            st.write(f"**Description:** {t['description']}")
            st.write(f"**Assigned To:** {t['manager_name']}")
            st.write(f"**Assignment Reason:** {t['assignment_reason']}")
            
            if t['status'] != 'Resolved':
                notes = st.text_area("Resolution Notes")
                if st.button("Mark as Resolved"):
                    from email_service import send_resolution_email
                    resolve_ticket(ticket_to_action, notes)
                    
                    # Send Email Notification
                    send_resolution_email(
                        user_email=t['user_id'],
                        ticket_id=t['ticket_id'],
                        ticket_title=t['title'],
                        resolution_notes=notes
                    )
                    
                    st.success("Ticket Resolved and User Notified!")
                    st.rerun()
            else:
                st.success(f"Assigned Resolution: {t['resolution_notes']}")
        
        # Logs Section
        st.markdown("#### Activity Logs")
        for _, log in logs.iterrows():
            with st.container(border=True):
                st.caption(f"{log['timestamp']} - {log['action']}")
                st.write(log['details'])

    # Visualization
    st.markdown("---")
    st.subheader("Analytics")
    c1, c2 = st.columns(2)
    with c1:
        fig = px.pie(tickets_df, names='status', title='Tickets by Status')
        st.plotly_chart(fig)
    with c2:
        fig = px.bar(tickets_df, x='category', color='severity', title='Tickets by Category and Severity')
        st.plotly_chart(fig)
