# your_app/management/commands/send_reminders.py
from django.core.management.base import BaseCommand
from user_profile.signals import *
from user_profile.models import *
from dms_module.models import *
from django.utils import timezone
from datetime import timedelta
import logging
import ipdb
import time
from user_profile.email_utils import *


logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Send reminders for documents based on action time, running continuously.'

    def handle(self, *args, **kwargs):
        logger.info("Reminder service started...")
        
        # Start the reminder loop
        while True:
            now = timezone.now()  # Get current time
            # Fetch all DocumentSendBackAction objects that have not had reminders sent
            actions = DocumentSendBackAction.objects.filter(reminder_sent=False)
            ipdb.set_trace()
            # Loop through actions and send reminders if the time has passed
            for action in actions:
                created_at = action.created_at
                user = action.document.assigned_to  # The user to receive the reminder

                # Get the reminder time intervals (in minutes) for the assigned user
                reminder_settings = ReminderAfterNoACtionTaken.objects.first()  # Assuming there's one global setting

                if reminder_settings:
                    # Loop through each reminder minute interval stored in reminder_minutes
                    for minutes in reminder_settings.reminder_minutes:
                        # Calculate the reminder time by adding the reminder minutes to the created_at time
                        reminder_time = created_at + timedelta(minutes=minutes)

                        # If the current time is greater than or equal to the reminder time, send the reminder email
                        if now >= reminder_time and not action.reminder_sent:
                            self.send_reminder(action)
                            action.reminder_sent = True  # Mark as reminder sent
                            action.save()

                            logger.info(f"Reminder sent to {user.email} for document '{action.document.document_title}'")

            # Sleep for 60 seconds before checking again
            time.sleep(60)

    def send_reminder(self, action):
        """ Helper method to send a reminder email. """
        user = action.document.assigned_to
        document_title = action.document.document_title
        ipdb.set_trace()
        # Send the email using the utility function (assumed to be defined)
        send_document_sendback_reminder_email(user, document_title)

        logger.info(f"Reminder email sent to {user.email} for document '{document_title}'")
