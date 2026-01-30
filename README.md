# 🤖 Trugen: AI Ticket Resolution System

Trugen is a streamlined customer support platform that leverages **AI Multi-Agent Systems (CrewAI)** to automatically triage, classify, and assign incoming support tickets.

## 🚀 Key Features

- **Multi-Agent Triage**: 5 specialized AI agents analyze every ticket for urgency, category, and technical implications.
- **Unified Interface**: Single navigation hub for both **Customer Portal** and **Admin Dashboard**.
- **Real-time Tracking**: Modern User UI to raise and track tickets with live activity timelines.
- **Admin Command Center**: Ticket management, analytics, and automated resolution email notifications.
- **Persistent Data**: Powered by **DuckDB** for ultra-fast local data storage.

## 🛠️ Tech Stack

- **Framework**: Streamlit
- **AI Orchestration**: CrewAI
- **LLM**: OpenAI (GPT-4o)
- **Database**: DuckDB
- **Automation**: SMTP Email Notifications

## 📥 Installation

1. **Clone the repository**:

   ```bash
   git clone <repo-url>
   cd ticket_resolution_system
   ```

2. **Install Dependencies** (using `uv` recommended):

   ```bash
   uv sync
   ```

3. **Configure Environment**:
   Create a `.env` file with the following:
   ```env
   OPENAI_API_KEY=your_key_here
   ADMIN_PASSWORD=admin123
   # Optional SMTP Settings for Emails
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your_email@gmail.com
   SMTP_PASSWORD=your_app_password
   ```

## 🏃 How to Run

Start the unified application:

```bash
uv run streamlit run app.py
```

## 📁 Project Structure

- `app.py`: Main entry point and navigation.
- `pages/`: Individual portal logic (User & Admin).
- `agents.py`: CrewAI agent definitions.
- `ticket_processor.py`: Orchestrates the AI analysis tasks.
- `database.py`: SQL operations and schema management.
- `email_service.py`: Automated notification logic.
