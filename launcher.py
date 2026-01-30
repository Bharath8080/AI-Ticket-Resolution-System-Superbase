import os
import subprocess
from database import init_db

def main():
    print("🚀 Initializing AI Ticket Resolution System...")
    
    # 1. Initialize Database
    print("📦 Setting up database...")
    init_db()
    
    print("\n✅ System initialized!")
    print("\nTo run the application, use:")
    print("uv run streamlit run app.py")
    
    print("\nNote: Make sure to update your .env file with your OPENAI_API_KEY.")

if __name__ == "__main__":
    main()
