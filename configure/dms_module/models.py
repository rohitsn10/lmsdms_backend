from django.db import models
from user_profile.models import *

class WorkFlowModel(models.Model):
    workflow_name = models.TextField(blank=True, null=True)
    workflow_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    

class DocumentType(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    document_name = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class PrintRequest(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='print_requests') 
    sop_document_id = models.ForeignKey("Document", on_delete=models.CASCADE,blank=True, null=True, related_name='print_requests')  # Updated
    no_of_print = models.IntegerField()  
    issue_type = models.TextField(blank=True, null=True)  
    reason_for_print = models.TextField(blank=True, null=True) 
    print_request_status = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    master_copy_user = models.ManyToManyField(CustomUser, related_name='master_copy_requests', blank=True)
    other_user = models.ManyToManyField(CustomUser, related_name='other_user_requests', blank=True)
    printer = models.ForeignKey("PrinterMachinesModel", on_delete=models.CASCADE,blank=True, null=True)  # Updated
    reminder_sent = models.BooleanField(default=False)
    reminder_sent_times = models.JSONField(default=list)


    
class PrintRequestApproval(models.Model):

    print_request = models.ForeignKey(PrintRequest, on_delete=models.CASCADE, related_name='approvals')  # Foreign key to PrintRequest
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='approved_print_requests')  # Foreign key to CustomUser (admin who approves)
    no_of_request_by_admin = models.IntegerField()  # Field for number of requests approved by admin
    status = models.ForeignKey('DynamicStatus', on_delete=models.CASCADE,blank=True, null=True)
    # approval_number = models.CharField(max_length=255, unique=True, blank=True, null=True)  # New field for unique number
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-populated created date
    approval_numbers = models.ManyToManyField('ApprovalNumber', blank=True)  # Many-to-many field for unique numbers
    retrival_numbers = models.ManyToManyField('RetrivalNumber', blank=True)  # Many-to-many field for unique numbers

class ApprovalNumber(models.Model):
    number = models.CharField(max_length=255, unique=True)  # Unique approval number
    created_at = models.DateTimeField(auto_now_add=True) 

class RetrivalNumber(models.Model):
    retrival_number = models.CharField(max_length=255, unique=True)  # Unique approval number
    created_at = models.DateTimeField(auto_now_add=True) 


class TemplateModel(models.Model):
    template_name = models.CharField(max_length=255)  
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    template_doc = models.FileField(upload_to='templates/') 
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True) 

    
class Document(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    document_title = models.TextField(blank=True, null=True) 
    document_number = models.CharField(max_length=255) 
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE) 
    document_description = models.TextField(blank=True, null=True)  
    revision_date = models.DateTimeField(blank=True, null=True)
    document_operation = models.TextField(blank=True, null=True)  
    form_status = models.TextField(blank=True, null=True)
    document_current_status = models.ForeignKey('DynamicStatus', on_delete=models.CASCADE,blank=True, null=True)
    select_template = models.ForeignKey(TemplateModel, on_delete=models.CASCADE, blank=True, null=True)
    assigned_to = models.ForeignKey(CustomUser, related_name="assigned_documents", on_delete=models.SET_NULL, blank=True, null=True)  # To track the user to whom the document is currently assigned 
    assigned_to_group = models.TextField(blank=True, null=True)    
    workflow = models.ForeignKey(WorkFlowModel, on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)
    version = models.CharField(max_length=10, default="1.0")
    is_revised = models.BooleanField(default=False)
    training_required = models.BooleanField(default=False)  # New field added
    last_action_time = models.DateTimeField(blank=True, null=True, default=None)
    visible_to_users = models.ManyToManyField(CustomUser, related_name="visible_documents")
    effective_date = models.DateTimeField(blank=True, null=True)  # New field added


    
class UploadedDocument(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)  
    word_file = models.FileField(upload_to='uploaded_docs/') 
    uploaded_at = models.DateTimeField(auto_now_add=True) 

    
class DocumentVersion(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="versions")
    version_number = models.CharField(max_length=10)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True)

    
class DynamicStatus(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class DocumentDetails(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)  
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    document_data = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    
class DocumentComments(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    Comment_description = models.JSONField(blank=True, null=True)    
    created_at = models.DateTimeField(auto_now_add=True)

class DocApprove(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE,blank=True, null=True)
    status_approve = models.ForeignKey(DynamicStatus, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class DocumentAuthorApproveAction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE,blank=True, null=True)
    # documentdetails_approve = models.ForeignKey(DocumentDetails, on_delete=models.CASCADE)  
    status_approve = models.ForeignKey(DynamicStatus, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class DocumentReviewerAction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE,blank=True, null=True)
    status_approve = models.ForeignKey(DynamicStatus, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class DocumentApproverAction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE,blank=True, null=True)
    status_approve = models.ForeignKey(DynamicStatus, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class DocumentDocAdminAction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE,blank=True, null=True)
    status_approve = models.ForeignKey(DynamicStatus, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class DocumentSendBackAction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True, null=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE,blank=True, null=True)
    status_sendback = models.ForeignKey(DynamicStatus, on_delete=models.CASCADE,blank=True, null=True)
    group = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    reminder_sent = models.BooleanField(default=False)
    reminder_sent_times = models.JSONField(default=list)

class DocumentReleaseAction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE,blank=True, null=True)
    status_release = models.ForeignKey(DynamicStatus, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class DocumentEffectiveAction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE,blank=True, null=True)
    status_effective = models.ForeignKey(DynamicStatus, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class DocumentRevisionAction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE,blank=True, null=True)
    status_revision = models.ForeignKey(DynamicStatus, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class DocumentRevisionRequestAction(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE,blank=True, null=True)
    revise_description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

class DynamicInventory(models.Model):
    inventory_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
class PrinterMachinesModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    printer_name = models.TextField(blank=True, null=True)
    printer_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
    

    
