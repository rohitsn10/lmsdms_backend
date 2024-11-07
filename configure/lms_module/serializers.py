     
from .models import *
from rest_framework import serializers
from django.contrib.auth.models import Group, Permission

class GetDepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ['id', 'department_name', 'department_description']

class GetPlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ['id', 'plant_name', 'plant_location', 'plant_description', 'plant_created_at']

class GetJobRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRole
        fields = ['job_role_name', 'job_role_description']

class GetAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id', 'area_name', 'department', 'area_description', 'area_created_at']

class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = '__all__' 

class AssessmentQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentQuestion
        fields = '__all__'

class MethodologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Methodology
        fields = ['id', 'methodology_name', 'methodology_created_at']

class TrainingTypeSerializer(serializers.ModelSerializer):
    created_by_name = serializers.ReadOnlyField(source='created_by.first_name')
    class Meta:
        model = TrainingType
        fields = ['id', 'training_type_name', 'created_by', 'created_by_name','training_type_created_at']

class TrainingCreateSerializer(serializers.ModelSerializer):
    plant_name = serializers.CharField(source='plant.plant_name', read_only=True)
    training_type_name = serializers.CharField(source='training_type.training_type_name', read_only=True)
    methodology_name = serializers.SerializerMethodField()  # Fixed this to handle ManyToMany properly
    document = serializers.SerializerMethodField()
    created_by_name = serializers.ReadOnlyField(source='created_by.first_name')

    class Meta:
        model = TrainingCreate
        fields = [
            'id', 'plant', 'plant_name', 'training_name', 'training_type', 'training_type_name',
            'training_number', 'training_title', 'training_version', 'refresher_time',
            'training_document', 'methodology', 'methodology_name', 'created_by', 'created_by_name',
            'training_created_at', 'training_updated_at'
        ]

    def get_document(self, obj):

        if obj.training_document and hasattr(obj.training_document, 'url'):
            request = self.context.get('request')
            return request.build_absolute_uri(obj.training_document.url)
        return None

    def get_methodology_name(self, obj):

        if obj.methodology.exists():
            return [methodology.methodology_name for methodology in obj.methodology.all()]
        return []
    

