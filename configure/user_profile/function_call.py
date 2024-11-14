import secrets
import string
import os
from django.utils import timezone
from django.conf import settings


def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def get_training_document_upload_path(filename):
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    file_extension = os.path.splitext(filename)[1]
    new_filename = f'{timestamp}{file_extension}'
    return os.path.join('training_documents', new_filename)