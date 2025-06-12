from flask import current_app
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.models import User
import logging

def send_incident_notification(incident, action):
    if not current_app.config['MAIL_USERNAME']:
        current_app.logger.warning('Email not configured - MAIL_USERNAME is empty')
        return
    
    current_app.logger.info(f'Preparing to send {action} notification for incident {incident.id}')
    
    creator = User.query.get(incident.created_by)
    assignee = User.query.get(incident.assigned_to) if incident.assigned_to else None
    
    # Different email content based on action
    if action == 'created':
        recipients = [u.email for u in User.query.filter_by(role='admin').all()]
        subject = f'New Incident Created: {incident.title}'
        body = f"""
        New incident created:
        Title: {incident.title}
        Priority: {incident.priority}
        Created by: {creator.username}
        Description: {incident.description}
        """
        current_app.logger.info(f'Created notification - Recipients: {recipients}')
    elif action == 'assigned':
        recipients = [creator.email]
        if assignee:
            recipients.append(assignee.email)
        subject = f'Incident Assigned: {incident.title}'
        body = f"""
        Incident assigned:
        Title: {incident.title}
        Assigned to: {assignee.username if assignee else 'Unassigned'}
        Priority: {incident.priority}
        """
        current_app.logger.info(f'Assignment notification - Recipients: {recipients}')
    elif action == 'resolved':
        recipients = [creator.email]
        if assignee:
            recipients.append(assignee.email)
        subject = f'Incident Resolved: {incident.title}'
        body = f"""
        Incident resolved:
        Title: {incident.title}
        Resolution notes: {incident.resolution_notes}
        """
        current_app.logger.info(f'Resolution notification - Recipients: {recipients}')
    
    # Create message
    message = f"""\
Subject: {subject}
To: {', '.join(recipients)}
From: {current_app.config['MAIL_DEFAULT_SENDER']}

{body}"""

    current_app.logger.info('Attempting to send email...')
    current_app.logger.info(f'SMTP settings: Server={current_app.config["MAIL_SERVER"]}, Port={current_app.config["MAIL_PORT"]}')
    
    try:
        with smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT']) as server:
            server.starttls()
            current_app.logger.info('Attempting to login...')
            server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
            current_app.logger.info('Login successful, sending email...')
            server.sendmail(
                current_app.config['MAIL_DEFAULT_SENDER'],
                recipients,
                message
            )
            current_app.logger.info('Email sent successfully!')
    except Exception as e:
        current_app.logger.error(f'Failed to send email: {str(e)}')
        current_app.logger.error(f'Error type: {type(e).__name__}')
        import traceback
        current_app.logger.error(f'Traceback: {traceback.format_exc()}') 