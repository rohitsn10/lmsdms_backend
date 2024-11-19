     
from .models import *
from rest_framework import serializers
from django.contrib.auth.models import Group, Permission

class GetDepartmentSerializer(serializers.ModelSerializer):
    department_created_at = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ['id', 'department_name', 'department_description', 'department_created_at']

    def get_department_created_at(self, obj):
        if obj.department_created_at:
            return obj.department_created_at.strftime('%d-%m-%Y')
        return None

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
    

class TrainingSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingSection
        fields = ['id', 'training', 'section_name', 'section_description', 'section_order']


class TrainingMaterialSerializer(serializers.ModelSerializer):
    material_file_url = serializers.SerializerMethodField()
    section = TrainingSectionSerializer(many=True)

    class Meta:
        model = TrainingMaterial
        fields = ['id', 'section', 'material_title', 'material_type', 'material_file_url', 'minimum_reading_time', 'material_created_at']

    def get_material_file_url(self, obj):
        request = self.context.get('request')
        if obj.material_file and hasattr(obj.material_file, 'url'):
            return request.build_absolute_uri(obj.material_file.url)
        return None
    

class TrainingQuestinSerializer(serializers.ModelSerializer):
    # Create custom fields to return URLs for audio and video files
    audio_file_url = serializers.SerializerMethodField()
    video_file_url = serializers.SerializerMethodField()

    class Meta:
        model = TrainingQuestions
        fields = [
            'id', 'training', 'question_type', 'question_text', 'options', 
            'correct_answer', 'marks', 'language', 'status', 
            'question_created_at', 'question_updated_at', 
            'created_by', 'updated_by', 'audio_file_url', 'video_file_url'
        ]

    def get_audio_file_url(self, obj):
        request = self.context.get('request')
        if obj.audio_file and hasattr(obj.audio_file, 'url'):
            return request.build_absolute_uri(obj.audio_file.url)
        return None

    def get_video_file_url(self, obj):
        request = self.context.get('request')
        if obj.video_file and hasattr(obj.video_file, 'url'):
            return request.build_absolute_uri(obj.video_file.url)
        return None
    

class QuizQuestionSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source='question.question_text')
    marks = serializers.IntegerField()

    class Meta:
        model = QuizQuestion
        fields = ['question', 'marks']

class TrainingQuizSerializer(serializers.ModelSerializer):
    questions = QuizQuestionSerializer(many=True)

    class Meta:
        model = TrainingQuiz
        fields = ['id', 'name', 'pass_criteria', 'quiz_time', 'total_marks', 'total_questions', 'quiz_type', 'questions', 'created_by','updated_by','created_at','updated_at','status']
class InductionSerializer(serializers.ModelSerializer):
    trainings = serializers.PrimaryKeyRelatedField(queryset=TrainingCreate.objects.all(), many=True)

    class Meta:
        model = Induction
        fields = ['id', 'plant', 'induction_name', 'trainings', 'created_at', 'updated_at']

class InductionDesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InductionDesignation
        fields = ['id', 'induction_designation_name', 'designation_code', 'induction', 'created_date', 'created_by']
        read_only_fields = ['created_date', 'created_by']        


class ClassroomTrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassroomTraining
        fields = [
            'id', 'classroom_type', 'title', 'description', 'department', 'employee',
            'document', 'sop', 'start_date', 'start_time', 'end_time',
            'created_at', 'created_by', 'status', 'acknowledgement', 'result'
        ]        

class TrainingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingCreate
        fields = ['id','plant', 'training_type', 'training_version', 'training_number', 'refresher_time']

class GetJobRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRole
        fields = ['id', 'job_role_name', 'job_role_description', 'plant', 'department', 'area']

class TrainingSerializer(serializers.ModelSerializer):
    methodology = serializers.StringRelatedField(many=True)

    class Meta:
        model = TrainingCreate
        fields = [
            "training_number","training_version","training_name","methodology","refresher_time",
        ]



