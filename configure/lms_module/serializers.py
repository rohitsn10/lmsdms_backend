     
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
