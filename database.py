import os
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def init_db():
    """
    Supabase tables should be created in the dashboard.
    This function will seed the 'managers' table if it's empty.
    """
    client = get_supabase_client()
    
    try:
        # Check if managers table has data
        response = client.table("managers").select("id", count="exact").execute()
        if response.count == 0:
            managers = [
                {"id": 1, "name": "Amit Patel", "role": "Support Lead", "department": "Customer Support"},
                {"id": 2, "name": "Anjali Singh", "role": "QA Lead", "department": "Quality Assurance"},
                {"id": 3, "name": "Priya Sharma", "role": "Backend Lead", "department": "Backend Engineering"},
                {"id": 4, "name": "Rajesh Kumar", "role": "SRE Lead", "department": "Infrastructure/SRE"},
                {"id": 5, "name": "Vikram Reddy", "role": "Security Lead", "department": "Security"}
            ]
            client.table("managers").insert(managers).execute()
    except Exception as e:
        print(f"⚠️ Error initializing/seeding database: {e}")

def add_user(user_id, name, email, phone):
    client = get_supabase_client()
    client.table("users").upsert({"id": user_id, "name": name, "email": email, "phone": phone}).execute()

def create_ticket(ticket_id, user_id, title, description, category=None):
    client = get_supabase_client()
    client.table("tickets").insert({
        "ticket_id": ticket_id,
        "user_id": user_id,
        "title": title,
        "description": description,
        "category": category,
        "status": "Open"
    }).execute()
    log_action(ticket_id, "Ticket Created", f"Ticket raised by user {user_id}")

def update_ticket_assignment(ticket_id, category, severity, priority, assigned_to_id, reason):
    client = get_supabase_client()
    client.table("tickets").update({
        "category": category,
        "severity": severity,
        "priority": priority,
        "assigned_to": assigned_to_id,
        "assignment_reason": reason,
        "status": "Assigned"
    }).eq("ticket_id", ticket_id).execute()
    log_action(ticket_id, "Ticket Assigned", f"Assigned to manager ID {assigned_to_id}. Reason: {reason[:100]}...")

def resolve_ticket(ticket_id, notes):
    client = get_supabase_client()
    client.table("tickets").update({
        "status": "Resolved",
        "resolved_at": datetime.now().isoformat(),
        "resolution_notes": notes
    }).eq("ticket_id", ticket_id).execute()
    log_action(ticket_id, "Ticket Resolved", notes)

def log_action(ticket_id, action, details):
    client = get_supabase_client()
    client.table("ticket_logs").insert({
        "ticket_id": ticket_id,
        "action": action,
        "details": details
    }).execute()

def get_all_tickets():
    client = get_supabase_client()
    # Join with managers using Supabase select syntax
    response = client.table("tickets").select("*, managers(name)").execute()
    df = pd.DataFrame(response.data)
    if not df.empty and 'managers' in df.columns:
        df['manager_name'] = df['managers'].apply(lambda x: x['name'] if x and 'name' in x else None)
    else:
         df['manager_name'] = None
    return df

def get_ticket_details(ticket_id):
    client = get_supabase_client()
    
    ticket_response = client.table("tickets").select("*, managers(name)").eq("ticket_id", ticket_id).execute()
    logs_response = client.table("ticket_logs").select("*").eq("ticket_id", ticket_id).order("timestamp", desc=True).execute()
    
    ticket_df = pd.DataFrame(ticket_response.data)
    if not ticket_df.empty and 'managers' in ticket_df.columns:
        ticket_df['manager_name'] = ticket_df['managers'].apply(lambda x: x['name'] if x and 'name' in x else None)
    
    logs_df = pd.DataFrame(logs_response.data)
    return ticket_df, logs_df

def get_managers():
    client = get_supabase_client()
    response = client.table("managers").select("*").eq("is_active", True).execute()
    return pd.DataFrame(response.data)
