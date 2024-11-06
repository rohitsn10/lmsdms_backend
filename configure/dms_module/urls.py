from django.urls import path
from dms_module.views import *


urlpatterns = [

   path('DashboardCount', DashboardCountViewSet.as_view({'get':'list'}),name='DashboardCount'),

   path('create_get_workflow', WorkFlowViewSet.as_view({'post': 'create','get':'list'}),name='create_get_workflow'),
   path('update_delete_workflow/<int:workflow_id>',WorkFlowUpdateSet.as_view({'put': 'update','delete':'destroy'}),name='update_delete_workflow'),
   
   path('create_get_document_type', DocumentTypeCreateViewSet.as_view({'post': 'create','get':'list'}),name='create_get_document_type'),
   path('create_get_workflow', WorkFlowViewSet.as_view({'post': 'create','get':'list'}),name='create_get_workflow'),
   path('update_delete_workflow/<int:workflow_id>',WorkFlowUpdateSet.as_view({'put': 'update','delete':'destroy'}),name='update_delete_workflow'),

   path('print_request', PrintRequestViewSet.as_view({'post': 'create','get':'list'}), name='print_request'),
   path('print_approvals', PrintApprovalViewSet.as_view({'post': 'create'}), name='print_approvals'),
   path('update_print_request/<int:print_request_id>', PrintRequestUpdateViewSet.as_view({'put': 'update'}), name='update_print_request'),
  
   path('create_document', DocumentCreateViewSet.as_view({'post': 'create'}),name='create_document'),
   path('update_document/<document_id>', DocumentUpdateViewSet.as_view({'put': 'update'}),name='update_document'),
   path('view_document', DocumentViewSet.as_view({'get':'list'}),name='view_document'),
   path('delete_Document', DocumentDeleteViewSet.as_view({'delete':'destroy'}),name='delete_Document'),

   path('create_template', TemplateCreateViewSet.as_view({'post': 'create'}),name='create_template'),
   path('update_template/<id>', TemplateUpdateViewSet.as_view({'put': 'update'}),name='update_template'),

   path('create_status', DynamicStatusCreateViewSet.as_view({'post': 'create'}),name='create_status'),
   path('view_status', DynamicStatusListViewSet.as_view({'get':'list'}),name='view_status'),
   path('update_status/<dynamic_status_id>', DynamicStatusUpdateViewSet.as_view({'put': 'update'}),name='update_status'),
   path('delete_status/<dynamic_status_id>', DynamicStatusDeleteViewSet.as_view({'delete':'destroy'}),name='delete_status'),

   path('create_document_details', DocumentDetailsCreateViewSet.as_view({'post': 'create'}),name='create_document_details'),
   path('update_document_details/<docdetail_id>', DocumentDetailsUpdateViewSet.as_view({'put': 'update'}),name='update_document_details'),
   path('view_document_details', DocumentDetailsViewSet.as_view({'get':'list'}),name='view_document_details'),

   path('document_approve_status', DocumentApproveActionCreateViewSet.as_view({'post': 'create'}),name='document_approve_status'),
   path('document_send_back_status', DocumentSendBackActionCreateViewSet.as_view({'post': 'create'}),name='document_send_back_status'),
   path('document_release_status', DocumentReleaseActionCreateViewSet.as_view({'post': 'create'}),name='document_release_status'),
   path('document_effective_status', DocumentEffectiveActionCreateViewSet.as_view({'post': 'create'}),name='document_effective_status'),

   path('UserDropdownMasterCopy', MasterCopyUserDropdownViewSet.as_view({'get':'list'}),name='UserDropdownMasterCopy'),
   path('UserDropdownOtherUser', OtherUserDropdownViewSet.as_view({'get':'list'}),name='UserDropdownOtherUser'),

   path('CreateInventory', DynamicInventoryCreateViewSet.as_view({'post': 'create'}), name='CreateInventory'),
   path('ViewInventory', DynamicInventoryListViewSet.as_view({'get': 'list'}), name='ViewInventory'),
   path('UpdateInventory/<inventory_id>', DynamicInventoryUpdateViewSet.as_view({'put': 'update'}), name='UpdateInventory'),
   path('DeleteInventory/<inventory_id>', DynamicInventoryDeleteViewSet.as_view({'delete': 'destroy'}), name='DeleteInventory'),

   path('CreateInventory', DocumentCommentCreateViewSet.as_view({'post': 'create'}), name='CreateInventory'),
   path('ViewInventory', DocumentCommentsViewSet.as_view({'get': 'list'}), name='ViewInventory'),
   path('DeleteInventory/<inventory_id>', DocumentCommentDeleteViewSet.as_view({'delete': 'destroy'}), name='DeleteInventory'),


]
