import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def send_resolution_email(user_email, ticket_id, ticket_title, resolution_notes):
    """
    Sends an email to the user when their ticket is resolved.
    SMTP settings are pulled from .env.
    """
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    if not all([smtp_server, smtp_port, smtp_user, smtp_password]):
        print(f"⚠️ SMTP settings missing in .env. Skipping email to {user_email}")
        print(f"DEBUG: Ticket {ticket_id} ('{ticket_title}') resolved with notes: {resolution_notes}")
        return False

    try:
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = user_email
        msg['Subject'] = f"Ticket Resolved: {ticket_id} - {ticket_title}"

        body = f"""
        Hello,

        Your support ticket has been resolved.

        Ticket ID: {ticket_id}
        Title: {ticket_title}
        
        Resolution Details:
        {resolution_notes}

        Thank you for your patience!

        Best Regards,
        Trugen Support Team
        """
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(smtp_server, int(smtp_port))
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Resolution email sent to {user_email}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        return False
