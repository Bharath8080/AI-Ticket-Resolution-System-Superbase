import duckdb
import os
from datetime import datetime

DB_PATH = "tickets.db"

def get_db_connection():
    return duckdb.connect(DB_PATH)

def init_db():
    conn = get_db_connection()
    
    # Create Users table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR PRIMARY KEY,
            name VARCHAR,
            email VARCHAR,
            phone VARCHAR
        )
    """)
    
    # Create Managers table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS managers (
            id INTEGER PRIMARY KEY,
            name VARCHAR,
            role VARCHAR,
            department VARCHAR,
            is_active BOOLEAN DEFAULT TRUE
        )
    """)
    
    # Seed Managers if empty
    res = conn.execute("SELECT COUNT(*) FROM managers").fetchone()[0]
    if res == 0:
        managers = [
            (1, 'Amit Patel', 'Support Lead', 'Customer Support'),
            (2, 'Anjali Singh', 'QA Lead', 'Quality Assurance'),
            (3, 'Priya Sharma', 'Backend Lead', 'Backend Engineering'),
            (4, 'Rajesh Kumar', 'SRE Lead', 'Infrastructure/SRE'),
            (5, 'Vikram Reddy', 'Security Lead', 'Security')
        ]
        for m in managers:
            conn.execute("INSERT INTO managers (id, name, role, department) VALUES (?, ?, ?, ?)", m)

    # Create Tickets table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id VARCHAR PRIMARY KEY,
            user_id VARCHAR,
            title VARCHAR,
            description VARCHAR,
            category VARCHAR,
            severity VARCHAR,
            priority VARCHAR,
            status VARCHAR DEFAULT 'Open',
            assigned_to INTEGER,
            assignment_reason TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            resolved_at TIMESTAMP,
            resolution_notes TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (assigned_to) REFERENCES managers(id)
        )
    """)
    
    # Create Ticket Logs table
    conn.execute("CREATE SEQUENCE IF NOT EXISTS log_id_seq")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS ticket_logs (
            id INTEGER PRIMARY KEY DEFAULT nextval('log_id_seq'),
            ticket_id VARCHAR,
            action VARCHAR,
            details TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.close()

def add_user(user_id, name, email, phone):
    conn = get_db_connection()
    conn.execute("INSERT OR IGNORE INTO users (id, name, email, phone) VALUES (?, ?, ?, ?)", 
                 (user_id, name, email, phone))
    conn.close()

def create_ticket(ticket_id, user_id, title, description, category=None):
    conn = get_db_connection()
    conn.execute("""
        INSERT INTO tickets (ticket_id, user_id, title, description, category, status) 
        VALUES (?, ?, ?, ?, ?, 'Open')
    """, (ticket_id, user_id, title, description, category))
    conn.close()
    log_action(ticket_id, "Ticket Created", f"Ticket raised by user {user_id}")

def update_ticket_assignment(ticket_id, category, severity, priority, assigned_to_id, reason):
    conn = get_db_connection()
    conn.execute("""
        UPDATE tickets 
        SET category = ?, severity = ?, priority = ?, assigned_to = ?, assignment_reason = ?, status = 'Assigned'
        WHERE ticket_id = ?
    """, (category, severity, priority, assigned_to_id, reason, ticket_id))
    conn.close()
    log_action(ticket_id, "Ticket Assigned", f"Assigned to manager ID {assigned_to_id}. Reason: {reason[:100]}...")

def resolve_ticket(ticket_id, notes):
    conn = get_db_connection()
    conn.execute("""
        UPDATE tickets 
        SET status = 'Resolved', resolved_at = CURRENT_TIMESTAMP, resolution_notes = ?
        WHERE ticket_id = ?
    """, (notes, ticket_id))
    conn.close()
    log_action(ticket_id, "Ticket Resolved", notes)

def log_action(ticket_id, action, details):
    conn = get_db_connection()
    conn.execute("INSERT INTO ticket_logs (ticket_id, action, details) VALUES (?, ?, ?)", 
                 (ticket_id, action, details))
    conn.close()

def get_all_tickets():
    conn = get_db_connection()
    df = conn.execute("""
        SELECT t.*, m.name as manager_name 
        FROM tickets t 
        LEFT JOIN managers m ON t.assigned_to = m.id
    """).fetchdf()
    conn.close()
    return df

def get_ticket_details(ticket_id):
    conn = get_db_connection()
    ticket = conn.execute("""
        SELECT t.*, m.name as manager_name 
        FROM tickets t 
        LEFT JOIN managers m ON t.assigned_to = m.id 
        WHERE t.ticket_id = ?
    """, (ticket_id,)).fetchdf()
    logs = conn.execute("SELECT * FROM ticket_logs WHERE ticket_id = ? ORDER BY timestamp DESC", (ticket_id,)).fetchdf()
    conn.close()
    return ticket, logs

def get_managers():
    conn = get_db_connection()
    managers = conn.execute("SELECT * FROM managers WHERE is_active = TRUE").fetchdf()
    conn.close()
    return managers
