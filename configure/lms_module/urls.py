from django.urls import path
from lms_module.views import *

urlpatterns = [

    path('create_get_department', DepartmentAddView.as_view({'post': 'create', 'get': 'list'}), name='create_get_department'),
    path('get_department', DepartmentAddView.as_view({'post': 'create', 'get': 'list'}), name='get_department'),
    path('update_delete_department/<int:department_id>', DepartmentUpdatesViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='update_delete_department'),

    path('create_get_plant', PlantAddView.as_view({'post': 'create', 'get': 'list'}), name='create_get_plant'),
    path('update_delete_plant/<int:plant_id>', PlantUpdatesViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='update_delete_plant'),

    path('create_get_job_role', JobRoleAddView.as_view({'post': 'create', 'get': 'list'}), name='create_get_job_role'),
    path('update_delete_job_role/<int:job_role_id>', JobRoleUpdatesViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='update_delete_job_role'),

    path('create_get_area', AreaAddView.as_view({'post': 'create', 'get': 'list'}), name='create_get_area'),
    path('update_delete_area/<int:area_id>', AreaUpdatesViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='update_delete_area'),

    path('create_get_assessment', AssessmentViewSet.as_view({'post': 'create', 'get': 'list'}), name='create_get_assessment'),
    path('update_assessment/<int:assessment_id>', AssessmentUpdateViewSet.as_view({'put': 'update'}), name='update_assessment'),

    path('create_get_assessment_question',AssessmentQuestionViewSet.as_view({'post': 'create', 'get': 'list'}),name='create_get_assessment_question'),
    path('update_assessment_question/<int:assessment_question_id>',AssessmentQuestionUpdateViewSet.as_view({'put': 'update'}),name='update_assessment_question'),

    path('create_methodology', MethodologyCreateViewSet.as_view({'post': 'create', 'get': 'list'}), name='create_methodology'),
    path('update_methodology/<int:methodology_id>', MethodologyUpdateViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='update_methodology'),

    path('create_training_type', TrainingTypeCreateViewSet.as_view({'post': 'create', 'get': 'list'}), name='create_training_type'),
    path('update_training_type/<int:training_type_id>', TrainingTypeUpdateViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='update_training_type'),

    path('create_training', TrainingCreateViewSet.as_view({'post': 'create', 'get': 'list'}), name='create_training'),
    path('update_training/<int:training_id>', TrainingUpdateViewSet.as_view({'put': 'update'}), name='update_training'),

    path('create_training_section', TrainingSectionViewSet.as_view({'post': 'create', 'get': 'list'}), name='create_section_data'),
    path('update_training_section/<int:training_section_id>', TrainingSectionUpdateViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='update_section_data'),

    path('create_training_material', TrainingMaterialCreateViewSet.as_view({'post': 'create', 'get': 'list'}), name='create_training_material'),
    path('update_training_material/<int:training_topic_id>', TrainingMaterialUpdateViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='update_training_material'),

    path('create_training_questions', TrainingQuestionCreateViewSet.as_view({'post': 'create', 'get': 'list'}), name='create_training_questions'),
    path('update_training_questions/<int:training_question_id>', TrainingQuestionUpdateViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='update_training_questions'),

    path('create_training_quiz', TrainingQuizCreateViewSet.as_view({'post': 'create', 'get': 'list'}), name='create_training_quiz'),
    path('update_training_quiz/<int:training_quiz_id>', TrainingQuizUpdateView.as_view({'put': 'update', 'delete': 'destroy'}), name='update_training_quiz'),
  
    path('create_induction', InductionCreateViewSet.as_view({'post': 'create', 'get': 'list'}), name='create_induction'),
    path('update_induction/<int:id>', InductionUpdateViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='update_induction'),

    path('create_induction_designation', InductionDesignationCreateViewSet.as_view({'post': 'create', 'get': 'list'}), name='create_induction_designation'),
    path('update_induction_designation/<int:id>', InductionDesignationUpdateViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='update_induction_designation'),

    path('create_classroom_training', ClassroomTrainingCreateViewSet.as_view({'post': 'create', 'get': 'list'}), name='create_classroom_training'),
    path('update_classroom_training/<int:id>', ClassroomTrainingUpdateViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='update_classroom_training'),
    path('mark_classroom_training_completed/<int:id>', ClassroomTrainingCreateViewSet.as_view({'post': 'mark_completed'}), name='mark_classroom_training_completed'),

    path('training_list', TrainingListViewSet.as_view({'get': 'list'}), name='training_list'),
    path('job_training_list', JobroleListingViewSet.as_view({'get': 'list'}), name='job_training_list'),
    path('jobrole_assign_training/<int:training_id>', TrainingAssignViewSet.as_view({'put': 'update'}), name='jobrole_assign_training'),


]
