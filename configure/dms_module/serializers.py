from rest_framework import serializers
from .models import *

class WorkFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkFlowModel
        fields = ['id', 'workflow_name', 'workflow_description', 'created_at', 'is_active']

class PrintRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrintRequest
        fields = ['id', 'user', 'sop_document_id', 'no_of_print', 'issue_type','reason_for_print','print_request_status','created_at']

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

class DocumentEffectiveActionSerializer(serializers.ModelSerializer):
    document = serializers.SerializerMethodField()
    class Meta:
        model = DocumentDetails
        fields = ['id', 'user','document','document_data', 'created_at']

    def get_document(self, obj):
        return DocumentSerializer(obj.document).data

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name']

class DynamicInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DynamicInventory
        fields = ['id', 'inventory_name', 'created_at', 'updated_at']

