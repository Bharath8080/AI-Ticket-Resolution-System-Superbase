from crewai import Task, Crew, Process
from agents import create_agents
from database import update_ticket_assignment, log_action
import json
import re

def process_ticket(ticket_data):
    """
    ticket_data: dictionary with ticket_id, title, description
    """
    ticket_id = ticket_data['ticket_id']
    title = ticket_data['title']
    description = ticket_data['description']
    
    agents = create_agents()
    triage_lead, support_analyst, sre_analyst, backend_analyst, tech_lead = agents
    
    # Define Tasks
    triage_task = Task(
        description=f"Analyze this ticket: Title: {title}, Description: {description}. Provide a concise summary and urgency assessment.",
        agent=triage_lead,
        expected_output="A summary of the ticket and urgency level."
    )
    
    classification_task = Task(
        description="Based on the triage summary, classify this ticket into one of: Payments, Technical, Access, Infrastructure, or General.",
        agent=support_analyst,
        expected_output="The classification category."
    )
    
    sre_task = Task(
        description="Analyze if this is an SRE/Infra issue. If so, explain why.",
        agent=sre_analyst,
        expected_output="Analysis of infra implications."
    )
    
    backend_task = Task(
        description="Analyze if this is a backend logic or database issue.",
        agent=backend_analyst,
        expected_output="Analysis of backend implications."
    )
    
    assignment_task = Task(
        description="""Synthesize all previous reports. 
        Determine:
        1. Final Category
        2. Severity (P0, P1, P2)
        3. Priority (High, Medium, Low)
        4. Assigned Manager ID (1-5)
        5. Reason for assignment
        
        Provide the output in JSON format:
        {
            "category": "...",
            "severity": "...",
            "priority": "...",
            "manager_id": 1,
            "reason": "..."
        }
        """,
        agent=tech_lead,
        context=[triage_task, classification_task, sre_task, backend_task],
        expected_output="A JSON object containing assignment details."
    )
    
    # Create Crew
    crew = Crew(
        agents=agents,
        tasks=[triage_task, classification_task, sre_task, backend_task, assignment_task],
        process=Process.sequential,
        verbose=True
    )
    
    # Execute
    log_action(ticket_id, "AI Analysis Started", "CrewAI agents are analyzing the ticket.")
    result = crew.kickoff()
    
    # Parse JSON result (Cleaning up if LLM adds markdown)
    raw_result = str(result)
    json_match = re.search(r'\{.*\}', raw_result, re.DOTALL)
    if json_match:
        try:
            data = json.loads(json_match.group())
            update_ticket_assignment(
                ticket_id=ticket_id,
                category=data.get('category'),
                severity=data.get('severity'),
                priority=data.get('priority'),
                assigned_to_id=data.get('manager_id'),
                reason=data.get('reason')
            )
            log_action(ticket_id, "AI Analysis Completed", "Ticket has been successfully assigned.")
        except Exception as e:
            log_action(ticket_id, "AI Analysis Error", f"Error parsing AI result: {str(e)}")
    else:
        log_action(ticket_id, "AI Analysis Error", "AI failed to produce a structured assignment.")
    
    return result
