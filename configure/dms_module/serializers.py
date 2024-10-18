from rest_framework import serializers
from .models import *

class WorkFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkFlowModel
        fields = ['id', 'workflow_name', 'workflow_description', 'created_at', 'is_active']


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ['id', 'user', 'document_name', 'created_at']