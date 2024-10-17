from django.urls import path
from lms_module.views import *

urlpatterns = [

    path('CreateGetDepartment', DepartmentAddView.as_view({'post': 'create', 'get': 'list'}), name='CreateGetDepartment'),
    path('UpdateDeleteDepartment/<int:department_id>', DepartmentUpdatesViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='UpdateDeleteDepartment'),

    path('CreateGetPlant', PlantAddView.as_view({'post': 'create', 'get': 'list'}), name='CreateGetPlant'),
    path('UpdateDeletePlant/<int:plant_id>', PlantUpdatesViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='UpdateDeletePlant'),

    path('CreateGetJobRole', JobRoleAddView.as_view({'post': 'create', 'get': 'list'}), name='CreateGetJobRole'),
    path('UpdateDeleteJobRole/<int:job_role_id>', JobRoleUpdatesViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='UpdateDeleteJobRole'),

    path('CreateGetArea', AreaAddView.as_view({'post': 'create', 'get': 'list'}), name='CreateGetArea'),
    path('UpdateDeleteArea/<int:area_id>', AreaUpdatesViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='UpdateDeleteArea'),


]
