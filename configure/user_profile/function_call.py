import secrets
import string
import os
from django.utils import timezone
from django.conf import settings
import decimal
import re
from django.db.models import Max
from dms_module.models import *
from datetime import datetime, timedelta


def validate_dates(start_date, end_date):
    date_format = '%d-%m-%Y'

    if not start_date or not end_date:
        return None, None, "Both Start Date and End Date are required."

    try:
        if start_date == end_date:
            start_date_obj = datetime.strptime(start_date, date_format).date()
            end_date_obj = start_date_obj + timedelta(days=1)
        else:
            start_date_obj = datetime.strptime(start_date, date_format).date()
            end_date_obj = datetime.strptime(end_date, date_format).date()
    except ValueError as e:
        return None, None, str(e)

    if start_date_obj > end_date_obj:
        return None, None, "start_date cannot be greater than end_date."

    return start_date_obj, end_date_obj, None


def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def get_training_document_upload_path(filename):
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    file_extension = os.path.splitext(filename)[1]
    new_filename = f'{timestamp}{file_extension}'
    return os.path.join('training_documents', new_filename)


def increment_version(version_str):
    major, minor = map(int, version_str.split('.'))
    minor += 1 
    if minor >= 10:
        minor = 0
        major += 1
    return f"{major}.{minor}"


def get_new_version(version_str):
        major, minor = map(int, version_str.split('.'))
        major += 1
        minor = 0
        
        return f"{major}.{minor}"




def generate_document_number(document_title, user, document_type, parent_document_instance=None):

    if user.department:
        department_name = user.department.department_name  # Access department_name correctly
    else:
        department_name = 'UnknownDepartment'  # Fallback if no department is assigned
    
    base_number = f"{document_title}/{department_name}/"
    
    if parent_document_instance is None:
        if document_type.id == 1:
            suffix_prefix = ""
        else:
            suffix_prefix = "001"

        last_document = Document.objects.filter(parent_document__isnull=True, document_type=document_type).order_by('-document_number').first()

        if last_document:
            last_suffix = last_document.document_number.split('/')[-1]
            if last_suffix.isdigit():
                next_suffix = str(int(last_suffix) + 1).zfill(3)
            else:
                prefix = last_suffix[0]
                num_part = int(last_suffix[1:])
                next_suffix = f"{prefix}{str(num_part + 1).zfill(3)}"
        else:
            next_suffix = f"{suffix_prefix}001"  # Default starting point if no documents exist

        document_number = base_number + next_suffix

    else:
        parent_document_number = parent_document_instance.document_number
        suffix_prefix = ""

        if document_type.id == 2:  # DocumentType 2 => "A001"
            suffix_prefix = "A"
        elif document_type.id == 3:  # DocumentType 3 => "F001"
            suffix_prefix = "F"
        
        last_document = Document.objects.filter(
            parent_document=parent_document_instance,
            document_type=document_type
        ).order_by('-document_number').first()

        if last_document:
            last_suffix = last_document.document_number.split('/')[-1]
            if last_suffix.isdigit():
                next_suffix = f"{suffix_prefix}{str(int(last_suffix[1:]) + 1).zfill(3)}"
            else:
                prefix = last_suffix[0]
                num_part = int(last_suffix[1:])
                next_suffix = f"{prefix}{str(num_part + 1).zfill(3)}"
        else:
            next_suffix = f"{suffix_prefix}001"  # Starting with A001 or F001

        document_number = f"{parent_document_number}/{next_suffix}"

    return document_number







