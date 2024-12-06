import threading
import time
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from user_profile.models import *
from dms_module.models import *
import logging
import pytz
from django.utils.dateformat import format

# Set up logging
logger = logging.getLogger(__name__)

# Global variable to track if the reminder thread is running
reminder_thread_running = False

def send_revision_reminder():
    global reminder_thread_running
    reminder_thread_running = True
    while True:
        current_time = timezone.now()

        # Find documents where revision_date is within 2 minutes and not revised
        reminder_documents = Document.objects.filter(
            revision_date__gt=current_time,
            is_revised=False  # Only send reminder if the document is not yet revised
        )

        # Fetch all reminder minutes from the Reminder table (assuming only one Reminder entry exists)
        try:
            reminder_obj = Reminder.objects.first()  # Fetch the first (and maybe only) reminder object
            if not reminder_obj:
                logger.warning("No reminder object found in the database.")
                continue
            reminder_minutes = reminder_obj.reminder_minutes  # Get the reminder minutes list
        except Exception as e:
            logger.error(f"Failed to fetch reminder minutes: {str(e)}")
            continue

        for document in reminder_documents:
            try:
                # Loop through each reminder minute
                for reminder in reminder_minutes:
                    reminder_time = document.revision_date - timedelta(minutes=reminder)
                    # Check if the current time is within the reminder window
                    if current_time >= reminder_time and current_time < reminder_time + timedelta(minutes=1):

                        user = document.user  # The user who created the document
                        department = user.department  # The department of the user

                        doc_admin_users = CustomUser.objects.filter(
                            department=department,
                            groups__name="doc_admin"
                        )
                        for doc_admin in doc_admin_users:
                            subject = f"Reminder: Document {document.document_title} Revision Due Soon"
                            message = f"Dear {doc_admin.first_name},\n\nThis is a reminder that the document '{document.document_title}' created by {user.first_name} is due for revision in 2 minutes. Please make sure to update it accordingly.\n\nBest regards,\nYour Team"
                            from_email = settings.EMAIL_HOST_USER
                            recipient_list = [doc_admin.email]

                            # Send the email to the 'doc_admin' user
                            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                            logger.info(f"Sent revision reminder email to {doc_admin.email} about document {document.document_title} created by {user.username}")

            except Exception as e:
                logger.error(f"Failed to send reminder email to doc_admin about document {document.document_title}: {str(e)}")

        time.sleep(60)  

def start_reminder_thread():
    global reminder_thread_running
    if not reminder_thread_running:
        threading.Thread(target=send_revision_reminder, daemon=True).start()

# Flag to prevent recursion
updating_document = False

@receiver(post_save, sender=Document)
def start_reminder_on_document_creation(sender, instance, created, **kwargs):
    global updating_document
    if updating_document:
        return  # Prevent recursion

    # Prevent recursion when saving the instance
    updating_document = True

    # Check if the revision_date needs to trigger a reminder
    current_time = timezone.now()
    needs_reminder = instance.revision_date > current_time and instance.revision_date <= current_time + timedelta(minutes=2)

    if created or not instance.is_revised or needs_reminder:  # Check if newly created or revision reminder needed
        logger.info(f"Creating or updating Document instance {instance.document_title}, starting reminder thread.")

        # If it's newly created or the revision date is near, send reminder
        start_reminder_thread()

        # Mark the document as not revised if it's created (or reset if needed)
        instance.is_revised = False
        instance.save(update_fields=['is_revised'])  # Reset is_revised to False if needed

    updating_document = False  # Reset the flag
