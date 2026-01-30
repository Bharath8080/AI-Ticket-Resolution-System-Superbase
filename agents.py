from crewai import Agent, LLM
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    return LLM(
        model="openai/gpt-4o",
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.7
    )

def create_agents():
    llm = get_llm()
    
    triage_lead = Agent(
        role='Triage Lead',
        goal='Analyze the raw customer ticket input to understand the core issue and context.',
        backstory="""You are an expert at understanding customer issues. 
        Your job is to read the ticket title and description and provide a clear summary of the problem, 
        detecting the tone and urgency.""",
        allow_delegation=False,
        llm=llm,
        verbose=True
    )
    
    support_analyst = Agent(
        role='Support Analyst',
        goal='Classify the ticket category and determine the basic domain (e.g., Billing, Account, Technical).',
        backstory="""You have years of experience in customer support. 
        You can quickly identify if a ticket is about a payment failure, password reset, or a general query.""",
        allow_delegation=False,
        llm=llm,
        verbose=True
    )
    
    sre_analyst = Agent(
        role='SRE Analyst',
        goal='Investigate infrastructure and reliability concerns such as server downtime or CDN issues.',
        backstory="""You are an infrastructure expert. You look for keywords like "timeout", "server error", 
        "slow loading", or "video buffering" to determine if the platform's reliability is affected.""",
        allow_delegation=False,
        llm=llm,
        verbose=True
    )
    
    backend_analyst = Agent(
        role='Backend Analyst',
        goal='Analyze potential database or server-side logic errors.',
        backstory="""You are a senior backend developer. You look for issues related to data not saving, 
        incorrect calculations, or API errors that aren't platform-wide infrastructure issues.""",
        allow_delegation=False,
        llm=llm,
        verbose=True
    )
    
    tech_lead = Agent(
        role='Tech Lead',
        goal='Synthesize all insights and officially assign the ticket to the best-suited manager.',
        backstory="""You are the ultimate decision-maker. You take the analysis from Triage, Support, SRE, and Backend agents.
        You then decide:
        1. The Category of the ticket.
        2. The Severity (P0, P1, P2) and Priority (High, Medium, Low).
        3. Which Manager to assign the ticket to based on their expertise.
        
        Available Managers:
        1. Amit Patel (Support Lead) - General queries, billing.
        2. Anjali Singh (QA Lead) - Bugs, UI issues.
        3. Priya Sharma (Backend Lead) - Server logic, DB issues.
        4. Rajesh Kumar (SRE Lead) - Infrastructure, performance, video playback.
        5. Vikram Reddy (Security Lead) - Access, data privacy.
        """,
        allow_delegation=True,
        llm=llm,
        verbose=True
    )
    
    return [triage_lead, support_analyst, sre_analyst, backend_analyst, tech_lead]
