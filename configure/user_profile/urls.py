from django.urls import path
from user_profile.views import *


urlpatterns = [
    path('group_id_wise_permission_list', GroupIdWisePermissionListAPIView.as_view(), name='group_id_wise_permission_list'),
    path('permission_list', PermissionListAPIView.as_view(), name='permission_list'),
    path('group_create_with_permissions', CreateGroupWithPermissionViewSet.as_view({'post':'create','get':'list'}), name='group_create_with_permissions'),
    path('group_update_with_permissions/<int:group_id>', UpdateGroupWithPermissionViewSet.as_view({'put':'update','get':'list'}), name='group_update_with_permissions'),
    path('group_delete/<int:group_id>', UpdateGroupWithPermissionViewSet.as_view({'delete':'destroy'}), name='group_delete'),

    path('user_create', CreateUserViewSet.as_view({'post':'create'}), name='user_create'),
    path('user_list', ListUserViewSet.as_view({'get':'list'}), name='user_list'),
    path('user_update/<int:user_id>', UpdateUserViewSet.as_view({'put':'update'}), name='user_update'),

]
