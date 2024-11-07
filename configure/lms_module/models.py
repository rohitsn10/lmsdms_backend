from django.db import models
from django.utils import timezone
from user_profile.models import CustomUser

class Plant(models.Model):
    plant_name = models.TextField()
    plant_location = models.TextField()
    plant_description = models.TextField()
    plant_created_at = models.DateTimeField(auto_now_add=True)

class Department(models.Model):
    department_name = models.TextField()
    department_description = models.TextField()
    department_created_at = models.DateTimeField(auto_now_add=True)

class Area(models.Model):
    area_name = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    area_description = models.TextField()
    area_created_at = models.DateTimeField(auto_now_add=True)

class JobRole(models.Model):
    job_role_name = models.TextField()
    job_role_description = models.TextField()

class Assessment(models.Model):
    title = models.TextField(blank=True, null=True)
    time_limit = models.TextField(blank=True, null=True)
    sop_selection = models.TextField(blank=True, null=True)
    assign = models.TextField(blank=True, null=True)  # For Department/Any user
    pass_percentage = models.TextField(blank=True, null=True)
    number_of_attempts = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class AssessmentQuestion(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='questions')
    sop = models.TextField(blank=True, null=True)  # Text field for SOP (Standard Operating Procedure)
    questions_data = models.JSONField()  # JSON field to store question, type, answers, etc.
    marks = models.TextField(blank=True, null=True)  # Text field for marks (e.g., "10 marks", "Pass/Fail", etc.)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"Assessment created by {self.created_by.full_name} on {self.created_at}"
    

class Methodology(models.Model):
    methodology_name = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    methodology_created_at = models.DateTimeField(auto_now_add=True)

class TrainingType(models.Model):
    training_type_name = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    training_type_created_at = models.DateTimeField(auto_now_add=True)


class TrainingCreate(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    training_type = models.ForeignKey(TrainingType, on_delete=models.CASCADE)
    training_number = models.CharField(max_length=255,null=True,blank=True)
    training_name = models.TextField()
    training_version = models.CharField(max_length=255,null=True,blank=True)
    refresher_time = models.DateField(null=True,blank=True)
    training_document = models.FileField(upload_to='training_documents/')
    methodology = models.ManyToManyField(Methodology)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    training_created_at = models.DateTimeField(auto_now_add=True)
    training_updated_at = models.DateTimeField(auto_now=True)
