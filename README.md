# 🤖 Trugen AI Support: Smart Ticket Resolution System

Trugen is a next-generation AI-powered ticket resolution system designed to streamline customer support using autonomous agents, cloud persistence, and a unified portal experience.

## ✨ Key Features

- **Unified Access Gateway**: A single entry point for both Customers and Admins with role-based routing.
- **Session-Based Auto-fill**: Customers log in once, and their contact details are automatically pre-filled in every ticket, saving time and ensuring accuracy.
- **Gemini 2.0 Flash Backend**: Powered by Google's latest high-speed LLM for rapid and intelligent ticket analysis.
- **Supabase Cloud Persistence**: Robust PostgreSQL-based data storage for tickets, users, and audit logs.
- **Autonomous Multi-Agent Analysis**: CrewAI agents work in the background to summarize, classify, and assign tickets to the right managers automatically.
- **Professional Dashboard**: Advanced analytics, ticket filtering, and management controls for support leads.
- **Automated Email Notifications**: Real-time SMTP alerts for users when their issues are resolved.

## 🛠️ Tech Stack

- **Framework**: [Streamlit](https://streamlit.io/) (Frontend/UI)
- **AI Orchestration**: [CrewAI](https://crewai.com/)
- **LLM**: Google Gemini 2.0 Flash (via `crewai[google-genai]`)
- **Database**: [Supabase](https://supabase.com/) (PostgreSQL)
- **Programming Language**: Python 3.10+
- **Environment Management**: [uv](https://github.com/astral-sh/uv)

## 📥 Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Bharath8080/AI-Ticket-Resolution-System-Superbase.git
   cd ticket_resolution_system
   ```

2. **Install Dependencies** (using `uv` is recommended):

   ```bash
   uv sync
   ```

3. **Configure Environment**:
   Create a `.env` file in the root directory:

   ```env
   # LLM Keys
   GEMINI_API_KEY=your_google_ai_studio_key

   # Database (Supabase)
   SUPABASE_URL=your_supabase_project_url
   SUPABASE_KEY=your_supabase_anon_key

   # Admin Security
   ADMIN_PASSWORD=your_admin_password

   # Email Service (Optional)
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your_email@gmail.com
   SMTP_PASSWORD=your_app_password

   # System Settings
   CREWAI_TELEMETRY_OPTOUT=true
   ```

## 🚀 Running the App

Start the Streamlit application:

```bash
uv run streamlit run app.py
```

## 📂 Project Structure

- `app.py`: Entry point with Unified Login and dynamic routing.
- `portals/`:
  - `user_portal.py`: Customer ticket submission and tracking.
  - `admin_dashboard.py`: Admin analytics and management.
- `agents.py`: CrewAI agent definitions using Gemini.
- `ticket_processor.py`: Background logic for multi-agent task orchestration.
- `database.py`: Supabase client and CRUD operations.
- `email_service.py`: Automated resolution alert system.
- `supabase_schema.sql`: Database initialization script.

## 🤝 Contributing

Feel free to fork this project, submit PRs, or report issues!

---

_Built with ❤️ by the Trugen Team_
