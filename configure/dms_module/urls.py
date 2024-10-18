from django.urls import path
from dms_module.views import *


urlpatterns = [


   path('CreateGetWorkflow', WorkFlowViewSet.as_view({'post': 'create','get':'list'}),name='CreateGetWorkflow'),
   path('UpdateDeleteWorkflow/<int:workflow_id>',WorkFlowUpdateSet.as_view({'put': 'update','delete':'destroy'}),name='UpdateDeleteWorkflow'),

    path('PrintRequest', PrintRequestViewSet.as_view({'post': 'create'}), name='PrintRequest'),
    path('PrintApprovals', PrintApprovalViewSet.as_view({'post': 'create'}), name='PrintApprovals'),
    path('UpdatePrintRequest/<int:print_request_id>', PrintRequestUpdateViewSet.as_view({'post': 'update'}), name='UpdatePrintRequest'),

]
