from django.db import models
from django.utils import timezone
from user_profile.models import CustomUser
from dms_module.models import *

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
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE,null=True,blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,null=True,blank=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE,null=True,blank=True)
    job_role_name = models.TextField(null=True,blank=True)
    job_role_description = models.TextField(null=True,blank=True)

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
    TRAINING_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    training_type = models.ForeignKey(TrainingType, on_delete=models.CASCADE)
    training_number = models.CharField(max_length=255,null=True,blank=True)
    training_name = models.TextField()
    training_version = models.CharField(max_length=255,null=True,blank=True)
    training_status = models.CharField(max_length=255,choices=TRAINING_STATUS_CHOICES,default='pending',null=True,blank=True)
    schedule_date = models.DateTimeField(null=True,blank=True)
    number_of_attempts = models.CharField(max_length=255,default='3',null=True,blank=True)
    refresher_time = models.DateField(null=True,blank=True)
    training_document = models.FileField(upload_to='training_documents/')
    methodology = models.ManyToManyField(Methodology)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    job_roles = models.ManyToManyField(JobRole)
    training_created_at = models.DateTimeField(auto_now_add=True)
    training_updated_at = models.DateTimeField(auto_now=True)


class TrainingSection(models.Model):
    training = models.ForeignKey(TrainingCreate, related_name='sections', on_delete=models.CASCADE)
    section_name = models.CharField(max_length=255)
    section_description = models.TextField(null=True, blank=True)
    section_order = models.CharField(max_length=255, default='1')
    reason_for_update = models.TextField(null=True, blank=True)
    training_section_active_status = models.BooleanField(default=True, null=True,blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='training_sections_created', null=True, blank=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='training_sections_updated',null=True, blank=True)
    section_created_at = models.DateTimeField(auto_now_add=True, null=True,blank=True)
    section_updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

    def __str__(self):
        return f"{self.section_name} - {self.training.training_name}"
    

class TrainingMaterial(models.Model):
    MATERIAL_CHOICES = (
        ('pdf', 'PDF'),
        ('image', 'Image'),
        ('audio', 'Audio'),
        ('video', 'Video'),
        ('html', 'HTML'),
        ('scorm', 'SCORM'),
        ('import', 'Import'),
    )
    section = models.ManyToManyField(TrainingSection)
    material_title = models.CharField(max_length=255)
    material_type = models.CharField(max_length=50, choices=MATERIAL_CHOICES)
    material_file = models.FileField(upload_to='training_materials/', null=True, blank=True)
    minimum_reading_time = models.CharField(max_length=500, null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='training_materials_created', null=True, blank=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='training_materials_updated', null=True, blank=True)
    material_created_at = models.DateTimeField(auto_now_add=True)
    material_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.material_title



class TrainingQuestions(models.Model):
    QUESTION_TYPE_CHOICES = (
        ('mcq', 'MCQ'),
        ('fill_in_the_blank', 'Fill in the blank'),
        ('true_false', 'True/False'),
    )

    training = models.ForeignKey(TrainingCreate, related_name='questions', on_delete=models.CASCADE)
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPE_CHOICES)
    audio_file = models.FileField(upload_to='audio_files/', null=True, blank=True)  # To store audio files
    video_file = models.FileField(upload_to='video_files/', null=True, blank=True)
    question_text = models.TextField()
    options = models.JSONField(null=True, blank=True)  # Store options for MCQ questions (as a list of strings)
    correct_answer = models.TextField()  # Store the correct answer (can be the option value or index)
    marks = models.PositiveIntegerField(default=1)  # Marks for the question
    language = models.CharField(max_length=50, default='en')  # Language of the question (default to English)
    status = models.BooleanField(default=True)  # Active/Inactive status
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='training_questions_created', null=True, blank=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='training_questions_updated', null=True, blank=True)
    question_created_at = models.DateTimeField(auto_now_add=True)
    question_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.question_text} - {self.training.training_name}"
    

class TrainingQuiz(models.Model):
    QUIZ_TYPE_CHOICES = (
        ('auto', 'Automatic'),
        ('manual', 'Manual'),
    )
    training = models.ForeignKey(TrainingCreate, related_name='quizzes', on_delete=models.CASCADE)
    quiz_name = models.CharField(max_length=255)
    pass_criteria = models.DecimalField(max_digits=5, decimal_places=2)  # For example, pass if >= 50%
    quiz_time = models.PositiveIntegerField()  # Time in minutes
    total_marks = models.PositiveIntegerField()
    total_questions = models.PositiveIntegerField()
    quiz_type = models.CharField(max_length=10, choices=QUIZ_TYPE_CHOICES)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='training_quizzes_created', null=True, blank=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='training_quizzes_updated', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True,null=True,blank=True)


    def __str__(self):
        return self.name

    def get_total_marks(self):
        return sum([q.marks for q in self.questions.all()])


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(TrainingQuiz, related_name="questions", on_delete=models.CASCADE)
    question = models.ForeignKey(TrainingQuestions, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()

    def __str__(self):
        return f"Quiz {self.quiz.id} - Question {self.question.id} ({self.marks} marks)"

# Code for induction create
class Induction(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    induction_name = models.CharField(max_length=255)
    trainings = models.ManyToManyField(TrainingCreate, related_name='inductions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.induction_name    
    

class InductionDesignation(models.Model):
    induction_designation_name = models.CharField(max_length=255)
    designation_code = models.CharField(max_length=50)
    induction = models.ForeignKey(Induction, on_delete=models.CASCADE, related_name='induction_designations')
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.induction_designation_name    
    

class ClassroomTraining(models.Model):
    TRAINING_TYPE_CHOICES = [
        ('with_assessment', 'With Assessment'),
        ('without_assessment', 'Without Assessment'),
    ]
    
    STATUS_CHOICES = [
        ('assigned', 'Assigned'),
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
    ]

    classroom_training_type = models.CharField(
        max_length=20, choices=TRAINING_TYPE_CHOICES
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    department_or_employee = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='classroom_trainings'
    )
    document = models.FileField(upload_to='classroom_trainings/', null=True, blank=True)
    sop = models.CharField(max_length=255)  # Assuming SOP refers to a string value
    start_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, related_name='created_classroom_trainings'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='assigned')
    acknowledged_by_employee = models.BooleanField(default=False)  # To track if employee acknowledged the training

    def __str__(self):
        return self.title


class TrainingMatrix(models.Model):
    EVALUATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    training = models.ForeignKey(TrainingCreate, on_delete=models.CASCADE)
    training_duration = models.DateTimeField(null=True, blank=True)
    evaluation_status = models.CharField(max_length=255, choices=EVALUATION_STATUS_CHOICES, null=True, blank=True)
    assigned_user = models.ManyToManyField(CustomUser)
    assigned_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    assigned_role = models.ForeignKey(JobRole, on_delete=models.CASCADE, null=True, blank=True)
    due_reason = models.TextField(null=True, blank=True)
    
    