# dashboard_app/email_utils.py
from django.core.mail import send_mail
from django.template import Template, Context
from django.utils.timezone import now
from django.conf import settings
from datetime import datetime
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group
import ipdb
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

def send_email_with_credentials(email, username, password, first_name):
    context = {
        'first_name': first_name,
        'username': username,
        'password': password,
    }
    send_dynamic_email('WELCOME_EMAIL', email, context)

def send_email_change_password(email, full_name):
    context = {
        'full_name': full_name,
        # 'support_url': 'https://bharatparantal.com/support'
    }
    send_dynamic_email('CHANGE_PASSWORD', email, context)



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


def send_document_sendback_reminder_email(assigned_to, document_title):
    context = {
        'full_name': f'{assigned_to.first_name} {assigned_to.last_name}',
        'document_title': document_title,
        'current_time': timezone.now().strftime('%d-%m-%Y'),
    }

    send_dynamic_email('DOCUMENT_SEND_BACK_REMINDER_NOTIFICATION', assigned_to.email, context)

    return {"status": True, "message": "Email sent successfully", "data": []}

def send_document_release_email(admin_user, documentdetails_release, status_release):
    context = {
        'full_name': f'{admin_user.first_name} {admin_user.last_name}',
        'document_title': documentdetails_release.document_title,
        'status_name': status_release.status,
        'current_time': timezone.now().strftime('%d-%m-%Y'),
    }

    send_dynamic_email('DOCUMENT_RELEASE_NOTIFICATION', admin_user.email, context)

def send_document_approval_email(user, document_title, recipients):
    for recipient in recipients:
        context = {
            'full_name': f'{recipient.first_name} {recipient.last_name}',
            'first_name': recipient.first_name,  
            'last_name': recipient.last_name,  
            'document_name': document_title,
            'current_time': timezone.now().strftime('%d-%m-%Y'),
        }

        send_dynamic_email('DOCUMENT_APPROVAL_NOTIFICATION', user.email, context)

def send_document_revise_email(user, documentdetails_revise, status_revise):
    context = {
        'receiver_first_name': user.first_name,
        'receiver_last_name': user.last_name, 
        'document_title': documentdetails_revise.document_title,
        'status_name': status_revise.status,
        'current_time': timezone.now().strftime('%d-%m-%Y'),
    }

    send_dynamic_email('DOCUMENT_REVISE_NOTIFICATION', user.email, context)

def send_print_request_email(user, no_of_print, reason_for_print, sop_document_id, issue_type, qa_users_in_department):
    current_time = timezone.now().strftime('%d-%m-%Y')
    # Loop through each user in qa_users_in_department
    for qa_user in qa_users_in_department:
        context = {
            'receiver_first_name': qa_user.first_name,
            'receiver_last_name': qa_user.last_name, 
            'document_title': sop_document_id.document_title,
            'no_of_print': no_of_print,
            'reason_for_print': reason_for_print,
            'issue_type': issue_type,
            'current_time': current_time,
        }

        # Send the email to each user individually
        send_dynamic_email('PRINT_REQUEST_NOTIFICATION', [qa_user.email], context)  # Pass only the current qa_user here


def send_reminder_email(assigned_user, document_title):
    # Email context
    subject = "Reminder: Take Action on Document"
    message = f"Dear {assigned_user.first_name},\n\nPlease take action on the document titled '{document_title}'.\nThis is a reminder to take action if you haven't done so yet."

    send_mail(subject, message, [assigned_user.email])

def send_print_request_reminder_email(qa_users_in_department, sop_document, no_of_print, reason_for_print, issue_type):
    current_time = timezone.now().strftime('%d-%m-%Y')
    # Loop through each user in qa_users_in_department
    for qa_user in qa_users_in_department:
        context = {
            'receiver_first_name': qa_user.first_name,
            'receiver_last_name': qa_user.last_name, 
            'document_title': sop_document.document_title,
            'no_of_print': no_of_print,
            'reason_for_print': reason_for_print,
            'issue_type': issue_type,
            'current_time': current_time,
        }

        # Send the email to each user individually
        send_dynamic_email('PRINT_REQUEST_REMINDER_NOTIFICATION', [qa_user.email], context)