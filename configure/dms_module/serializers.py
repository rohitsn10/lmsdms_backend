from rest_framework import serializers
from .models import *

class WorkFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkFlowModel
        fields = ['id', 'workflow_name', 'workflow_description', 'created_at', 'is_active']

class PrintRequestSerializer(serializers.ModelSerializer):
    document_title = serializers.CharField(source='sop_document_id.document_title', read_only=True)

    class Meta:
        model = PrintRequest
        fields = ['id', 'user', 'sop_document_id', 'document_title','no_of_print', 'issue_type','reason_for_print','print_request_status','created_at']

class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ['id', 'user', 'document_name', 'created_at']

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class DocumentdataSerializer(serializers.ModelSerializer):
    template_url = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ['id', 'select_template', 'template_url']

    def get_template_url(self, obj):
        request = self.context.get('request')
        if obj.select_template and obj.select_template.template_doc:
            return request.build_absolute_uri(obj.select_template.template_doc.url)
        return None
    

class TemplateDocumentSerializer(serializers.ModelSerializer):
    document_url = serializers.SerializerMethodField()

    class Meta:
        model = TemplateModel
        fields = ['template_name', 'document_url']

    def get_document_url(self, obj):
        request = self.context.get('request')
        if obj.template_doc:
            return request.build_absolute_uri(obj.template_doc.url)
        return None

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateModel
        fields = '__all__'

class DocumentviewSerializer(serializers.ModelSerializer):
    document_type_name = serializers.SerializerMethodField()
    formatted_created_at = serializers.SerializerMethodField()
    current_status_name = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ['id', 'document_title', 'document_number', 'formatted_created_at', 'document_type_name','form_status','document_current_status','current_status_name']

    def get_document_type_name(self, obj):
        return obj.document_type.document_name if obj.document_type else None

    def get_formatted_created_at(self, obj):
        return obj.created_at.strftime('%d-%m-%Y')
    
    def get_current_status_name(self, obj):
        return obj.document_current_status.status if obj.document_current_status else None

class DocumentCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentComments
        fields = ['id', 'user', 'document', 'Comment_description', 'created_at']

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

class DocumentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id','document_title','document_number','document_type','document_description','revision_time','revision_date','document_operation','select_template','workflow']

