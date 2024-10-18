from django.db import models
from user_profile.models import *

class WorkFlowModel(models.Model):
    workflow_name = models.TextField(blank=True, null=True)
    workflow_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.workflow_name
    

class DocumentType(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    document_name = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class PrintRequest(models.Model):
    STATUS_CHOICES = [
    ('done', 'Done'),
    ('pending', 'Pending'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='print_requests')  # Foreign key to CustomUser
    sop_document_id = models.TextField(blank=True, null=True)  # Text field for reason for print
    no_of_print = models.IntegerField()  # Field for the number of prints
    issue_type = models.TextField(blank=True, null=True)  # Text field for issue type
    reason_for_print = models.TextField(blank=True, null=True)  # Text field for reason for print
    print_request_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # Status field for print request
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-populated created date

    def __str__(self):
        return f"Print Request by {self.user.username} on {self.created_at}"
    
class PrintRequestApproval(models.Model):
    STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]
    print_request = models.ForeignKey(PrintRequest, on_delete=models.CASCADE, related_name='approvals')  # Foreign key to PrintRequest
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='approved_print_requests')  # Foreign key to CustomUser (admin who approves)
    no_of_request_by_admin = models.IntegerField()  # Field for number of requests approved by admin
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='approved')  # Status field for approval or rejection
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-populated created date

    def __str__(self):
        return f"Approval for Print Request ID {self.print_request.id} by {self.user.username} on {self.created_at}"
