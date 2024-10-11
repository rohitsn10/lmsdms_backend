from django.db import models

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