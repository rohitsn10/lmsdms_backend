# dashboard_app/email_utils.py
from django.core.mail import send_mail
from django.template import Template, Context
from django.utils.timezone import now
from django.conf import settings
from datetime import datetime
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group

import threading

def send_email_in_background(subject, message, from_email, recipient_list):
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

def send_dynamic_email(template_name, to_emails, context):
    from .models import EmailTemplate
    try:
        template = EmailTemplate.objects.get(name=template_name)
    except EmailTemplate.DoesNotExist:
        return {"status": False, "message": f"Email template '{template_name}' not found", "data": []}

    subject = template.subject
    content_template = Template(template.content)
    current_time = timezone.now().strftime('%d-%m-%Y')
    context['current_time'] = current_time
    context['signature'] = template.signature
    message = content_template.render(Context(context))
    from_email = template.from_email

    if isinstance(to_emails, list):
        for email in to_emails:
            threading.Thread(target=send_email_in_background, args=(subject, message, from_email, [email])).start()
    else:
        threading.Thread(target=send_email_in_background, args=(subject, message, from_email, [to_emails])).start()

    return {"status": True, "message": "Emails sent successfully", "data": []}

def send_email_forgot_password(email, full_name, username, otp):
    context = {
        'full_name': full_name,
        'username': username,
        'otp': otp
    }
    send_dynamic_email('FORGOT_PASSWORD', email, context)

def send_user_email(email, full_name, username):
    context = {
        'full_name': full_name,
        'username': username,
        'login_url': 'http://127.0.0.1:8000/login'
    }
    send_dynamic_email('WELCOME_EMAIL', email, context)

def send_email_change_password(email, full_name):
    context = {
        'full_name': full_name,
        # 'support_url': 'https://bharatparantal.com/support'
    }
    send_dynamic_email('CHANGE_PASSWORD', email, context)


# email_utils.py

def send_document_create_email(user, document_name, recipients):
    for recipient in recipients:
        context = {
            'full_name': f'{recipient.first_name} {recipient.last_name}',
            'first_name': recipient.first_name,  
            'last_name': recipient.last_name,  
            'document_name': document_name,
            'current_time': timezone.now().strftime('%d-%m-%Y'),
        }

        send_dynamic_email('DOCUMENT_CREATED', recipient.email, context)

    return {"status": True, "message": "Emails sent successfully", "data": []}


def send_document_update_email(user, document_name, recipients):
    for recipient in recipients:
        context = {
            'full_name': f'{recipient.first_name} {recipient.last_name}',
            'first_name': recipient.first_name,  
            'last_name': recipient.last_name,  
            'document_name': document_name,
            'current_time': timezone.now().strftime('%d-%m-%Y'),
        }

        send_dynamic_email('DOCUMENT_UPDATED', recipient.email, context)

    return {"status": True, "message": "Emails sent successfully", "data": []}


def send_document_sendback_email(assigned_to, document_title):
    context = {
        'full_name': f'{assigned_to.first_name} {assigned_to.last_name}',
        'document_title': document_title,
        'current_time': timezone.now().strftime('%d-%m-%Y'),
    }

    send_dynamic_email('DOCUMENT_SEND_BACK_NOTIFICATION', assigned_to.email, context)

    return {"status": True, "message": "Email sent successfully", "data": []}

