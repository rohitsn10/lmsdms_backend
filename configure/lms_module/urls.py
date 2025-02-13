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
    path('update_training_material/<int:training_material_id>', TrainingMaterialUpdateViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='update_training_material'),

    path('create_training_questions', TrainingQuestionCreateViewSet.as_view({'post': 'create', 'get': 'list'}), name='create_training_questions'),
    path('update_training_questions/<int:training_question_id>', TrainingQuestionUpdateViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='update_training_questions'),

    path('active_deactive_question/<int:question_id>', ActiveDeactiveQuestionViewSet.as_view({'put': 'update'}), name='update_training_questions'),

    path('training_wise_questions/<int:document_id>', TrainingIdWiseQuestionsViewSet.as_view({'get': 'list'}), name='training_wise_questions'),

    path('create_training_quiz', TrainingQuizCreateViewSet.as_view({'post': 'create', 'get': 'list'}), name='create_training_quiz'),
    path('list_training_quiz/<int:document_id>', TrainingQuizList.as_view({'get': 'list'}), name='create_training_quiz'),
    path('update_training_quiz/<int:training_quiz_id>', TrainingQuizUpdateView.as_view({'put': 'update', 'delete': 'destroy'}), name='update_training_quiz'),

    path('create_induction', InductionCreateViewSet.as_view({'post': 'create', 'get': 'list'}), name='create_induction'),
    path('update_induction/<int:id>', InductionUpdateViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='update_induction'),

    path('create_induction_designation', InductionDesignationCreateViewSet.as_view({'post': 'create', 'get': 'list'}), name='create_induction_designation'),
    path('update_induction_designation/<int:id>', InductionDesignationUpdateViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='update_induction_designation'),

    path('create_classroom', ClassroomCreateViewSet.as_view({'post': 'create', 'get': 'list'}), name='create_classroom_training'),
    path('update_classroom/<int:id>', ClassroomUpdateViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='update_classroom_training'),
    # path('update_classroom_training/<int:id>', ClassroomTrainingUpdateViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='update_classroom_training'),
    # path('mark_classroom_training_completed/<int:id>', ClassroomTrainingCreateViewSet.as_view({'post': 'mark_completed'}), name='mark_classroom_training_completed'),
    path('create_session', SessionCreateViewSet.as_view({'post': 'create', 'get': 'list'}), name='createsession'),
    path('session_completed/<int:session_id>', SessionCompletedViewSet.as_view({'post': 'mark_completed'}), name='session_completed'),
    path('update_session/<int:id>/', SessionUpdateViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name = 'updatesession'),
    
    path('attendance', AttendanceCreateViewSet.as_view({'post': 'create', 'get': 'list'}), name='attendance'),

    path('failed_user', FailedUserViewSet.as_view({'get': 'list'}), name='failed_user'),

    path('training_list', TrainingListViewSet.as_view({'get': 'list'}), name='training_list'),
    path('job_training_list', JobroleListingViewSet.as_view({'get': 'list'}), name='job_training_list'),
    path('jobrole_assign_training/<int:user_id>', TrainingAssignViewSet.as_view({'put': 'update'}), name='jobrole_assign_training'),

    path('training_matrix_assign_user_and_add_data', TrainingMatrixAssignUserViewSet.as_view({'post': 'create', 'get': 'list'}), name='training_list_mapping'),
    path('training_id_wise_training_section', TrainingIdWiseTrainingSectionViewset.as_view({'get': 'list'}), name='training_id_wise_training_section'),
    path('training_section_wise_training_material', TrainingSectionWiseTrainingMaterialViewset.as_view({'get': 'list'}), name='training_section_wise_training_material'),
    path('training_wise_training_matrix', TrainingWiseTrainingMatrixViewset.as_view({'get': 'list'}), name='training_wise_training_matrix'),

    path('job_training_list_mapping', JobroleListingapiViewSet.as_view({'get': 'list'}), name='job_training_list_mapping'),
    path('training_list_data', TrainingListingViewSet.as_view({'get': 'list'}), name='training_list_data'),
    path('training_assign_jobrole', TrainingAssigntoJobroleViewSet.as_view({'post': 'create', 'get': 'list'}), name='training_assign_jobrole'),

    path('classroom_questions', ClassroomQuestionViewSet.as_view({'post': 'create', 'get': 'list'}), name='classroom_questions'),
    path('classroom_quiz', ClassroomQuizViewSet.as_view({'post': 'create', 'get': 'list'}), name='classroom_quiz'),
    path('classroom_exam', ClassroomExamViewSet.as_view({'post': 'create'}), name='classroom_exam'),
    path('classroom_get_next_question', ClassroomGetNextQuestionViewSet.as_view({'get': 'list'}), name='classroom_get_next_question'),
    path('classroom_get_next_question_update', ClassroomUpdateGetNextQuestionViewSet.as_view({'put': 'update'}), name='classroom_get_next_question_update'),

    path('classroom_id_wise_question<int:classroom_id>', ClassroomIdWiseQuestionsViewSet.as_view({'get': 'list'}), name='classroom_id_wise_question'),

    path('training_status_update/<int:training_id>', TrainingStatusUpdateViewset.as_view({'put': 'update'}), name='training_status_update'),

    path('start_exam', StartExam.as_view({'post': 'create'}), name='start_exam'),
    path('get_next_question/<int:session_id>', GetNextQuestion.as_view({'get': 'list','put': 'update'}), name='get_next_question'),

    path('hracnowledgement/<int:user_id>', HrAcknowledgementViewSet.as_view({'post': 'create', 'get': 'list'}), name='hracnowledgement'),

    path('inductioncertificate/<int:user_id>', InductionCertificateViewSet.as_view({'post': 'create'}), name='inductioncertificate'),

    path('trainer_create', TrainerViewSet.as_view({'post': 'create', 'get': 'list'}), name='trainer_create'),
    path('trainer_update/<int:trainer_id>', TrainerViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='trainer_update'),

    path('jobdescriptioncreate', JobDescriptionCreateViewSet.as_view({'post': 'create'}), name='jobdescriptioncreate'),
    path('jobdescription_list/<int:user_id>', JobDescriptionList.as_view({'get': 'list'}), name='jobdescription_list'),
    path('hod_remarks/<int:job_description_id>',HODApprovalViewSet.as_view({'put': 'update'}), name='hod_remarks'),

    path('attempted_quiz', AttemptedQuizViewSet.as_view({'post': 'create'}), name='attempted_quiz'),
    path('attempted_quiz_list/<int:user_id>', AttemptedQuizListViewSet.as_view({'get': 'list'}), name='attempted_quiz_list'),
]
