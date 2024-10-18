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

