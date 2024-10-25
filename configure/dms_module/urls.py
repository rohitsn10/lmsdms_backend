from django.urls import path
from dms_module.views import *


urlpatterns = [

   path('create_get_workflow', WorkFlowViewSet.as_view({'post': 'create','get':'list'}),name='create_get_workflow'),
   path('update_delete_workflow/<int:workflow_id>',WorkFlowUpdateSet.as_view({'put': 'update','delete':'destroy'}),name='update_delete_workflow'),
   
   path('create_get_department', DocumentTypeCreateViewSet.as_view({'post': 'create','get':'list'}),name='create_get_department'),
   path('CreateGetWorkflow', WorkFlowViewSet.as_view({'post': 'create','get':'list'}),name='CreateGetWorkflow'),
   path('UpdateDeleteWorkflow/<int:workflow_id>',WorkFlowUpdateSet.as_view({'put': 'update','delete':'destroy'}),name='UpdateDeleteWorkflow'),


    path('PrintRequest', PrintRequestViewSet.as_view({'post': 'create'}), name='PrintRequest'),
    path('PrintApprovals', PrintApprovalViewSet.as_view({'post': 'create'}), name='PrintApprovals'),
    path('UpdatePrintRequest/<int:print_request_id>', PrintRequestUpdateViewSet.as_view({'post': 'update'}), name='UpdatePrintRequest'),


   path('CreateDocument', DocumentCreateViewSet.as_view({'post': 'create'}),name='CreateDocument'),
   path('UpdateDocument/<document_id>', DocumentUpdateViewSet.as_view({'put': 'update'}),name='UpdateDocument'),
   path('ViewDocument', DocumentViewSet.as_view({'get':'list'}),name='ViewDocument'),
   path('DeleteDocument', DocumentDeleteViewSet.as_view({'delete':'destroy'}),name='ViewDocument'),
   
   path('CreateTemplate', TemplateCreateViewSet.as_view({'post': 'create'}),name='CreateTemplate'),
   path('UpdateTemplate/<id>', TemplateUpdateViewSet.as_view({'put': 'update'}),name='UpdateTemplate'),

   path('CreateStatus', DynamicStatusCreateViewSet.as_view({'post': 'create'}),name='CreateStatus'),
   path('ViewStatus', DynamicStatusListViewSet.as_view({'get':'list'}),name='ViewStatus'),
   path('UpdateStatus/<dynamic_status_id>', DynamicStatusUpdateViewSet.as_view({'put': 'update'}),name='UpdateStatus'),
   path('DeleteStatus/<dynamic_status_id>', DynamicStatusDeleteViewSet.as_view({'delete':'destroy'}),name='DeleteStatus'),

   path('CreateDocumentDetails', DocumentDetailsCreateViewSet.as_view({'post': 'create'}),name='CreateDocumentDetails'),
   path('UpdateDocumentDetails/<docdetail_id>', DocumentDetailsUpdateViewSet.as_view({'put': 'update'}),name='UpdateDocumentDetails'),
   path('ViewDocumentDetails', DocumentDetailsViewSet.as_view({'get':'list'}),name='ViewDocumentDetails'),

   path('DocumentApproveStatus', DocumentApproveActionCreateViewSet.as_view({'post': 'create'}),name='DocumentApproveStatus'),
   path('DocumentSendBackStatus', DocumentSendBackActionCreateViewSet.as_view({'post': 'create'}),name='DocumentSendBackStatus'),
   path('DocumentReleaseStatus', DocumentReleaseActionCreateViewSet.as_view({'post': 'create'}),name='DocumentReleaseStatus'),
   path('DocumentEffectiveStatus', DocumentEffectiveActionCreateViewSet.as_view({'post': 'create'}),name='DocumentEffectiveStatus'),



]
