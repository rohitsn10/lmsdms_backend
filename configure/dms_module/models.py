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

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='print_requests')  # Foreign key to CustomUser
    sop_document_id = models.TextField(blank=True, null=True)  # Text field for reason for print
    no_of_print = models.IntegerField()  # Field for the number of prints
    issue_type = models.TextField(blank=True, null=True)  # Text field for issue type
    reason_for_print = models.TextField(blank=True, null=True)  # Text field for reason for print
    print_request_status = models.TextField(blank=True, null=True)  # Status field for print request
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-populated created date

    def __str__(self):
        return f"Print Request by {self.user.username} on {self.created_at}"
    
class PrintRequestApproval(models.Model):

    print_request = models.ForeignKey(PrintRequest, on_delete=models.CASCADE, related_name='approvals')  # Foreign key to PrintRequest
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='approved_print_requests')  # Foreign key to CustomUser (admin who approves)
    no_of_request_by_admin = models.IntegerField()  # Field for number of requests approved by admin
    status = models.TextField(blank=True, null=True)  # Status field for approval or rejection
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-populated created date

    def __str__(self):
        return f"Approval for Print Request ID {self.print_request.id} by {self.user.username} on {self.created_at}"

class TemplateModel(models.Model):
    template_name = models.CharField(max_length=255)  
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    template_doc = models.FileField(upload_to='templates/') 
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.template_name
    
class Document(models.Model):
   
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    document_title = models.TextField(blank=True, null=True) 
    document_number = models.CharField(max_length=255) 
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE) 
    document_description = models.TextField(blank=True, null=True)  
    revision_time = models.CharField(max_length=50, blank=True, null=True)  
    document_operation = models.TextField(blank=True, null=True)  
    select_template = models.ForeignKey(TemplateModel, on_delete=models.CASCADE, blank=True, null=True) 
    workflow = models.ForeignKey(WorkFlowModel, on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.document_title
    
class UploadedDocument(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)  
    word_file = models.FileField(upload_to='uploaded_docs/') 
    uploaded_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Uploaded document for {self.document.document_title}"
    
    
class DynamicStatus(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"{self.user.username} -: {self.status}"
    
class DocumentDetails(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)  
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    document_data = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document for {self.user.username} at {self.created_at}"



class DocumentApproveAction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    documentdetails = models.ForeignKey(DocumentDetails, on_delete=models.CASCADE)  
    status = models.ForeignKey(DynamicStatus, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    
