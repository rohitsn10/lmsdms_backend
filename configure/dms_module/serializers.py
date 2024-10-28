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

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class DynamicStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DynamicStatus
        fields = ['id', 'user', 'status', 'created_at', 'updated_at']

class DocumentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentDetails
        fields = ['id', 'user', 'document_data', 'created_at']

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name']
