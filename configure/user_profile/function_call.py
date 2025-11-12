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
from rest_framework.request import Request


def validate_dates(start_date, end_date):
    date_format = '%d-%m-%Y'

    if not start_date or not end_date:
       if not start_date and not end_date:
        return None, None, None  # No error, return None for dates
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


# def increment_version(version_str):
#     major, minor = map(int, version_str.split('.'))
#     minor += 1 
#     if minor >= 10:
#         minor = 0
#         major += 1
#     return f"{major}.{minor}"

def increment_version(version_str):
    major, minor = map(int, version_str.split('.'))
    minor += 1  # Just increment minor without rolling over
    return f"{major}.{minor}"


def get_new_version(version_str):
        major, minor = map(int, version_str.split('.'))
        major += 1
        minor = 0
        
        return f"{major}.{minor}"




# def generate_document_number(user, document_type, parent_document_instance=None):

#     if user.department:
#         department_name = user.department.department_name  # Access department_name correctly
#     else:
#         department_name = 'UnknownDepartment'
#     document_title = "BPL"
#     base_number = f"{document_title}/{department_name}/"
    
#     if parent_document_instance is None:
#         if document_type.id == 1:
#             suffix_prefix = ""
#         else:
#             suffix_prefix = "001"

#         last_document = Document.objects.filter(parent_document__isnull=True, document_type=document_type).order_by('-document_number').first()

#         if last_document:
#             last_suffix = last_document.document_number.split('/')[-1]
#             if last_suffix.isdigit():
#                 next_suffix = str(int(last_suffix) + 1).zfill(3)
#             else:
#                 prefix = last_suffix[0]
#                 num_part = int(last_suffix[1:])
#                 next_suffix = f"{prefix}{str(num_part + 1).zfill(3)}"
#         else:
#             next_suffix = f"{suffix_prefix}001"  # Default starting point if no documents exist

#         document_number = base_number + next_suffix

#     else:
#         parent_document_number = parent_document_instance.document_number
#         suffix_prefix = ""

#         if document_type.id == 2:  # DocumentType 2 => "A001"
#             suffix_prefix = "A"
#         elif document_type.id == 3:  # DocumentType 3 => "F001"
#             suffix_prefix = "F"
        
#         last_document = Document.objects.filter(
#             parent_document=parent_document_instance,
#             document_type=document_type
#         ).order_by('-document_number').first()

#         if last_document:
#             last_suffix = last_document.document_number.split('/')[-1]
#             if last_suffix.isdigit():
#                 next_suffix = f"{suffix_prefix}{str(int(last_suffix[1:]) + 1).zfill(3)}"
#             else:
#                 prefix = last_suffix[0]
#                 num_part = int(last_suffix[1:])
#                 next_suffix = f"{prefix}{str(num_part + 1).zfill(3)}"
#         else:
#             next_suffix = f"{suffix_prefix}001"  # Starting with A001 or F001

#         document_number = f"{parent_document_number}/{next_suffix}"

#     return document_number



# def generate_document_number(user, document_type, parent_document_instance=None):
#     # Access the department name
#     if user.department:
#         department_name = user.department.department_name  # Access department_name correctly
#     else:
#         department_name = 'UnknownDepartment'
    
#     document_title = "BPL"
#     base_number = f"{document_title}/{department_name}/"
    
#     # Case 1: Parent document is None (or blank), and document_type.id == 1
#     if parent_document_instance is None and document_type.id == 1:
#         # Get the document with the largest number for document_type.id == 1
#         last_document = Document.objects.filter(document_type=document_type).order_by('-document_number').first()
        
#         # Extract the numeric part from the last document number
#         if last_document:
#             last_suffix = last_document.document_number.split('/')[-1]  # Get the number part after the last "/"
#             if last_suffix.isdigit():
#                 # Increment the number by 1 and zero-pad it to 3 digits
#                 next_suffix = str(int(last_suffix) + 1).zfill(3)
#             else:
#                 # Handle cases where suffix might have non-numeric characters (e.g., "A001")
#                 prefix = last_suffix[0]
#                 num_part = int(last_suffix[1:])
#                 next_suffix = f"{prefix}{str(num_part + 1).zfill(3)}"
#         else:
#             # Default starting point if no documents exist
#             next_suffix = "001"  # Start with 001 if no document of this type exists
        
#         document_number = base_number + next_suffix

#     else:
#         # Case 2: Parent document is provided (for document types 2 or 3)
#         parent_document_number = parent_document_instance.document_number
#         suffix_prefix = ""

#         if document_type.id == 2:  # DocumentType 2 => "A001"
#             suffix_prefix = "A"
#         elif document_type.id == 3:  # DocumentType 3 => "F001"
#             suffix_prefix = "F"

#         last_document = Document.objects.filter(
#             parent_document=parent_document_instance,
#             document_type=document_type
#         ).order_by('-document_number').first()

#         if last_document:
#             last_suffix = last_document.document_number.split('/')[-1]
#             if last_suffix.isdigit():
#                 next_suffix = f"{suffix_prefix}{str(int(last_suffix[1:]) + 1).zfill(3)}"
#             else:
#                 prefix = last_suffix[0]
#                 num_part = int(last_suffix[1:])
#                 next_suffix = f"{prefix}{str(num_part + 1).zfill(3)}"
#         else:
#             next_suffix = f"{suffix_prefix}001"  # Starting with A001 or F001

#         document_number = f"{parent_document_number}/{next_suffix}"

#     return document_number


def generate_document_number(user, document_type, parent_document_instance=None):
    department_name = user.department.department_name if user.department else "UnknownDepartment"

    # SOP (1) and Format (2)
    prefix_mapping = {
        1: {
            "General Manufacturing Tablet Section": "SPGTA",
            "General Manufacturing Capsule Section": "SPGCA",
            "General Manufacturing Injection Section": "SPGIN",
            "General Manufacturing Liquid Orals Section": "SPGLI",
            "General Manufacturing Dry Powder/Oral Powder Section": "SPGDP",
            "External Preparation": "SPGEP",
            "General Manufacturing Store": "SPGST",
            "Beta-Lactam Manufacturing Tablet Section": "SPBTA",
            "Beta-Lactam Manufacturing Capsule Section": "SPBCA",
            "Beta-Lactam Manufacturing Injection Section": "SPBIN",
            "Beta-Lactam Manufacturing Dry Powder/Oral Powder Section": "SPBDP",
            "Beta-Lactam Manufacturing Store": "SPBST",
            "Cephalosporins Manufacturing Tablet Section": "SPCTA",
            "Cephalosporins Manufacturing Capsule Section": "SPCCA",
            "Cephalosporins Manufacturing Injection Section": "SPCIN",
            "Cephalosporins Manufacturing Dry Powder/Oral Powder Section": "SPCDP",
            "Cephalosporins Manufacturing Store": "SPCST",
            "Quality Control Chemical": "SPQCC",
            "Quality Control - Micro": "SPQCM",
            "Quality Assurnace": "SPQAD",
            "Enginerring": "SPENG",
            "HR & Admin": "SPHRA",
            "Artwork": "SPART",
            "Information & Technology": "SPITD",
        },
        3: {
            "General Manufacturing Tablet Section": "FGTA",
            "General Manufacturing Capsule Section": "FGCA",
            "General Manufacturing Injection Section": "FGIN",
            "General Manufacturing Liquid Orals Section": "FGLI",
            "General Manufacturing Dry Powder/Oral Powder Section": "FGDP",
            "External Preparation": "FGEP",
            "General Manufacturing Store": "FGST",
            "Beta-Lactam Manufacturing Tablet Section": "FBTA",
            "Beta-Lactam Manufacturing Capsule Section": "FBCA",
            "Beta-Lactam Manufacturing Injection Section": "FBIN",
            "Beta-Lactam Manufacturing Dry Powder/Oral Powder Section": "FBDP",
            "Beta-Lactam Manufacturing Store": "FBST",
            "Cephalosporins Manufacturing Tablet Section": "FCTA",
            "Cephalosporins Manufacturing Capsule Section": "FCCA",
            "Cephalosporins Manufacturing Injection Section": "FCIN",
            "Cephalosporins Manufacturing Dry Powder/Oral Powder Section": "FCDP",
            "Cephalosporins Manufacturing Store": "FCST",
            "Quality Control Chemical": "FQC",
            "Quality Control - Micro": "FQM",
            "Quality Assurnace": "FQA",
            "Enginerring": "FENG",
            "HR & Admin": "FHRA",
            "Artwork": "FART",
            "Information & Technology": "FITD",
        },
        14: {  # BMR Docs
            "General Manufacturing Tablet Section": "BMRGTA",
            "General Manufacturing Capsule Section": "BMRGCA",
            "General Manufacturing Injection Section": "BMRGIN",
            "General Manufacturing Liquid Orals Section": "BMRGLI",
            "General Manufacturing Dry Powder/Oral Powder Section": "BMRGDP",
            "External Preparation": "BMRGEP",
            "Beta-Lactam Manufacturing Tablet Section": "BMRBTA",
            "Beta-Lactam Manufacturing Capsule Section": "BMRBCA",
            "Beta-Lactam Manufacturing Injection Section": "BMRBIN",
            "Beta-Lactam Manufacturing Dry Powder/Oral Powder Section": "BMRBDP",
            "Cephalosporins Manufacturing Tablet Section": "BMRCTA",
            "Cephalosporins Manufacturing Capsule Section": "BMRCCA",
            "Cephalosporins Manufacturing Injection Section": "BMRCIN",
            "Cephalosporins Manufacturing Dry Powder/Oral Powder Section": "BMRCDP",
        }
    }

    # QA special (4–13)
    qa_special_mapping = {
        4: "IQ",
        5: "OQ",
        6: "PQ",
        7: "IOQ",
        8: "OPQ",
        9: "RQ",
        10: "PVPR",
        11: "HTPR",
        12: "CVP",
        13: "CVR"
    }

    # Fixed (15–21) - no department condition
    fixed_document_type_mapping = {
        15: "RMSPC",
        16: "PMSPC",
        17: "FPSPC",
        18: "RMSTP",
        19: "PMSTP",
        20: "FPSTP",
        21: "MISPR"
    }

    # Check fixed types first
    if document_type.id in fixed_document_type_mapping:
        prefix = fixed_document_type_mapping[document_type.id]

        last_document = Document.objects.filter(
            document_type=document_type,
            document_number__startswith=prefix
        ).order_by('-document_number').first()

        if last_document:
            last_suffix = last_document.document_number.replace(prefix, "")
            next_number = str(int(last_suffix) + 1).zfill(4)
        else:
            next_number = "0001"

        return f"{prefix}{next_number}"

    # QA Special case (4–13) for QA dept
    if department_name == "Quality Assurance" and document_type.id in qa_special_mapping:
        prefix = qa_special_mapping[document_type.id]

        last_document = Document.objects.filter(
            document_type=document_type,
            document_number__startswith=prefix
        ).order_by('-document_number').first()

        if last_document:
            last_suffix = last_document.document_number.replace(prefix, "")
            next_number = str(int(last_suffix) + 1).zfill(4)
        else:
            next_number = "0001"

        return f"{prefix}{next_number}"

    # SOP / Format / BMR (top level)
    if parent_document_instance is None and document_type.id in prefix_mapping:
        prefix = prefix_mapping.get(document_type.id, {}).get(department_name, "UNKNOWN")

        last_document = Document.objects.filter(
            document_type=document_type,
            document_number__startswith=prefix
        ).order_by('-document_number').first()

        if last_document:
            last_suffix = last_document.document_number.replace(prefix, "")
            next_number = str(int(last_suffix) + 1).zfill(4)
        else:
            next_number = "0001"

        return f"{prefix}{next_number}"

    # Sub-documents: types like id=2 or 3 that go under parent
    if parent_document_instance:
        parent_document_number = parent_document_instance.document_number
        suffix_prefix = ""

        if document_type.id == 2:
            suffix_prefix = "A"
        elif document_type.id == 3:
            suffix_prefix = "F"

        last_document = Document.objects.filter(
            parent_document=parent_document_instance,
            document_type=document_type
        ).order_by('-document_number').first()

        if last_document:
            last_suffix = last_document.document_number.split('/')[-1]
            next_suffix = f"{suffix_prefix}{str(int(last_suffix[1:]) + 1).zfill(3)}"
        else:
            next_suffix = f"{suffix_prefix}001"

        return f"{parent_document_number}/{next_suffix}"

    # Fallback
    return "UNKNOWN0001"



def get_file_data(request: Request, obj, field_name: str):
    # Get the field (ManyToManyField in this case) from the model instance
    field = getattr(obj, field_name, None)

    if field:
        # If it's a ManyToMany field (i.e., the field is a Manager), iterate over all related objects
        if isinstance(field, models.Manager):
            return [
                {
                    "id": str(item.id),
                    "url": request.build_absolute_uri(item.material_file.url),  # Assuming 'material_file' is the field in TrainingMaterialAttachments
                    "created_at": item.created_at.isoformat(),
                    "updated_at": item.updated_at.isoformat(),
                }
                for item in field.all()
            ]
    return None


# import fitz  # PyMuPDF

# import os
# import subprocess
# import platform

# def print_pdf_with_one_copy(pdf_path, printer_name=None):
#     """
#     Sends a PDF file to a printer and forces printing only 1 copy.
#     Works on both Linux (CUPS) and Windows (Win32 API).
#     """
#     try:
#         if not os.path.exists(pdf_path):
#             raise FileNotFoundError(f"PDF file not found: {pdf_path}")
#         os_type = platform.system()
#         print(f"Operating System: {os_type}")
#         print(f"PDF Path: {pdf_path}")
#         if os_type == "Linux":
#             print("Checking CUPS Printer List:")
#             # ✅ Use CUPS (Common Unix Printing System) for Linux
#             command = ["lp", "-n", "1", pdf_path]  # "-n 1" ensures 1 copy
#             if printer_name:
#                 command.insert(2, "-d")  # "-d printer_name" for specific printer
#                 command.insert(3, printer_name)
#             subprocess.run(command, check=True)

#         elif os_type == "Windows":
#             import win32print
#             import win32api

#             # ✅ Use Win32 API for Windows
#             if not printer_name:
#                 printer_name = win32print.GetDefaultPrinter()

#             print(f"Using Printer: {printer_name}")
#             win32api.ShellExecute(0, "print", pdf_path, f'/D:"{printer_name}"', ".", 0)

#         return True
#     except Exception as e:
#         print("Printing failed:", str(e))
#         return False

