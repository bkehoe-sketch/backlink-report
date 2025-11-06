import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import sys
sys.path.append('.')
from config.settings import *

def send_report_email(report_path):
    """Send the generated report via email"""
    
    subject = f"{REPORT_TITLE} - {CURRENT_DATE}"
    
    body = f"""
    Hi there,

    Your monthly backlink report for {TARGET_DOMAIN} is ready!

    This automated report includes:
    • Total backlinks and referring domains
    • Monthly growth metrics
    • New vs lost backlinks analysis
    • Historical trend charts

    Please find the detailed report attached.

    Best regards,
    Your Automated Backlink Reporter
    """
    
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        with open(report_path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= backlink_report_{CURRENT_DATE}.html'
            )
            msg.attach(part)
    except Exception as e:
        print(f"Error attaching report: {e}")
        return False
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_FROM, EMAIL_TO, text)
        server.quit()
        
        print(f"Email sent successfully to {EMAIL_TO}")
        return True
        
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

if __name__ == "__main__":
    if os.path.exists(REPORT_FILENAME):
        send_report_email(REPORT_FILENAME)
    else:
        print(f"Report file not found: {REPORT_FILENAME}")
