import threading
import time
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from user_profile.models import CustomUser
from dms_module.models import Document, Reminder
import logging
import pytz
from django.core.management.base import BaseCommand

# Set up logging
logger = logging.getLogger(__name__)

# Global variable to track if the reminder thread is running
reminder_thread_running = False

class Command(BaseCommand):
    help = 'Send revision reminders to doc_admin users based on document revision dates'

    def handle(self, *args, **options):
        """Handle the command logic"""
        self.stdout.write(self.style.SUCCESS("Starting the revision reminder process..."))
        self.run_reminder_thread()

    def run_reminder_thread(self):
        """Start a background thread to send revision reminders."""
        global reminder_thread_running

        reminder_thread_running = True

        def send_revision_reminder():
            while reminder_thread_running:
                current_time = timezone.now()

                # Fetch all reminder objects (in case there are multiple reminder objects stored in the DB)
                reminder_objects = Reminder.objects.all()

                if not reminder_objects:
                    logger.warning("No reminder object found in the database.")
                    time.sleep(60)  # Sleep for a minute before checking again
                    continue

                # Fetch documents that need reminders based on revision_date and is_revised
                reminder_documents = Document.objects.filter(
                    revision_date__gt=current_time,
                    is_revised=False  # Only send reminder if the document is not yet revised
                )

                for reminder_obj in reminder_objects:
                    reminder_minutes = reminder_obj.reminder_minutes  # Get the list of reminder minutes

                    for document in reminder_documents:
                        try:
                            # Loop through each reminder minute
                            for reminder in reminder_minutes:
                                reminder_time = document.revision_date - timedelta(minutes=reminder)

                                # Check if the current time is within the reminder window
                                if current_time >= reminder_time and current_time < reminder_time + timedelta(minutes=1):
                                    # Find the user who created the document
                                    user = document.user  # The user who created the document
                                    department = user.department  # Get the department of the document creator

                                    # Find the 'doc_admin' users from the same department
                                    doc_admin_users = CustomUser.objects.filter(
                                        department=department,
                                        groups__name='doc_admin'  # Assuming the 'doc_admin' group exists
                                    )

                                    # Send reminder emails to doc_admin users
                                    for doc_admin in doc_admin_users:
                                        subject = f"Reminder: Document '{document.document_title}' Revision Due Soon"
                                        message = f"Dear {doc_admin.username},\n\nThis is a reminder that the document '{document.document_title}' created by {user.username} is due for revision in {reminder} minutes. Please make sure to update it accordingly.\n\nBest regards,\nYour Team"
                                        from_email = settings.EMAIL_HOST_USER
                                        recipient_list = [doc_admin.email]

                                        # Send the email to the 'doc_admin' user
                                        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                                        logger.info(f"Sent revision reminder email to {doc_admin.email} about document '{document.document_title}' created by {user.username} for {reminder} minutes")

                        except Exception as e:
                            logger.error(f"Failed to send reminder email to doc_admin about document {document.document_title}: {str(e)}")

                # Sleep for a minute before checking again
                time.sleep(60)

        # Start the background thread for reminders
        reminder_thread = threading.Thread(target=send_revision_reminder)
        reminder_thread.daemon = True  # Set as a daemon so it will exit when the main process exits
        reminder_thread.start()
        self.stdout.write(self.style.SUCCESS("Revision reminder thread has started..."))
