from django.urls import path
from dms_module.views import *


urlpatterns = [


   path('create_get_workflow', WorkFlowViewSet.as_view({'post': 'create','get':'list'}),name='create_get_workflow'),
   path('update_delete_workflow/<int:workflow_id>',WorkFlowUpdateSet.as_view({'put': 'update','delete':'destroy'}),name='update_delete_workflow'),
   
   path('create_get_department', DocumentTypeCreateViewSet.as_view({'post': 'create','get':'list'}),name='create_get_department'),

]
