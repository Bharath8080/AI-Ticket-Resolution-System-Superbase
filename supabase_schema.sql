-- 1. Create Users table
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    name TEXT,
    email TEXT,
    phone TEXT
);

-- 2. Create Managers table
CREATE TABLE IF NOT EXISTS managers (
    id SERIAL PRIMARY KEY,
    name TEXT,
    role TEXT,
    department TEXT,
    is_active BOOLEAN DEFAULT TRUE
);

-- 3. Create Tickets table
CREATE TABLE IF NOT EXISTS tickets (
    ticket_id TEXT PRIMARY KEY,
    user_id TEXT REFERENCES users(id),
    title TEXT,
    description TEXT,
    category TEXT,
    severity TEXT,
    priority TEXT,
    status TEXT DEFAULT 'Open',
    assigned_to INTEGER REFERENCES managers(id),
    assignment_reason TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    resolved_at TIMESTAMPTZ,
    resolution_notes TEXT
);

-- 4. Create Ticket Logs table
CREATE TABLE IF NOT EXISTS ticket_logs (
    id BIGSERIAL PRIMARY KEY,
    ticket_id TEXT REFERENCES tickets(ticket_id),
    action TEXT,
    details TEXT,
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

-- Note: Enable Row Level Security (RLS) if needed, 
-- or disable it for testing in the Supabase Dashboard.
