from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from django.core.validators import validate_email
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import AccessToken, OutstandingToken
from rest_framework import status
from django.contrib.auth import logout
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from django.contrib.auth.models import Group, Permission
from django_filters.rest_framework import DjangoFilterBackend
from user_profile.function_call import *
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
import random
import ipdb
from lms_module.models import Department
from user_profile.email_utils import *


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    lookup_url_kwarg = 'pk'
    

class GroupIdWisePermissionListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    # filterset_class = PermissionFilter
   
    def get(self, request):
        # if not request.user.has_perm('auth.view_permission'):
        #     return Response({'status': False, 'message': "You don't have permission to perform this action"})

        group_id = request.query_params.get('group_id')
        user = request.user

        group_permissions_ids = []
        if group_id is not None:
            try:
                group = Group.objects.get(id=group_id)
                group_permissions_ids = group.permissions.values_list('id', flat=True)
            except Group.DoesNotExist:
                return Response({'status': False, 'message': 'Group not found!'})

        # Get all available permissions for the model
        all_permissions = Permission.objects.filter(group=group_id)
        permission_dict = {}

        for permission in all_permissions:
            model_name = permission.content_type.model
            if model_name not in permission_dict:
                permission_dict[model_name] = {
                    'name': model_name,
                    'isAdd': False,
                    'add': None,
                    'isChange': False,
                    'change': None,
                    'isDelete': False,
                    'delete': None,
                    'isView': False,
                    'view': None,
                }

            # Check which permission is available and update the dictionary
            # Additionally, check if the permission is in the specified group
            if permission.codename == f'add_{model_name}':
                permission_dict[model_name]['isAdd'] = permission.id in group_permissions_ids
                permission_dict[model_name]['add'] = permission.id
            elif permission.codename == f'change_{model_name}':
                permission_dict[model_name]['isChange'] = permission.id in group_permissions_ids
                permission_dict[model_name]['change'] = permission.id
            elif permission.codename == f'delete_{model_name}':
                permission_dict[model_name]['isDelete'] = permission.id in group_permissions_ids
                permission_dict[model_name]['delete'] = permission.id
            elif permission.codename == f'view_{model_name}':
                permission_dict[model_name]['isView'] = permission.id in group_permissions_ids
                permission_dict[model_name]['view'] = permission.id

        # Convert dictionary to a list
        permission_data = list(permission_dict.values())

        return Response({
            'status': True,
            'message': 'Permission List!',
            'data': permission_data
        })


class PermissionListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # if not request.user.has_perm('auth.view_permission'):
            #     return Response({'status': False, 'message': "You don't have permission to perform this action"})

            user = request.user

            group_permissions_ids = []

            # Get all available permissions for the model
            all_permissions = Permission.objects.all()
            permission_dict = {}

            for permission in all_permissions:
                model_name = permission.content_type.model
                if model_name not in permission_dict:
                    permission_dict[model_name] = {
                        'name': model_name,
                        'isAdd': False,
                        'add': None,
                        'isChange': False,
                        'change': None,
                        'isDelete': False,
                        'delete': None,
                        'isView': False,
                        'view': None,
                    }

                # Check which permission is available and update the dictionary
                # Additionally, check if the permission is in the specified group
                if permission.codename == f'add_{model_name}':
                    permission_dict[model_name]['isAdd'] = permission.id in group_permissions_ids
                    permission_dict[model_name]['add'] = permission.id
                elif permission.codename == f'change_{model_name}':
                    permission_dict[model_name]['isChange'] = permission.id in group_permissions_ids
                    permission_dict[model_name]['change'] = permission.id
                elif permission.codename == f'delete_{model_name}':
                    permission_dict[model_name]['isDelete'] = permission.id in group_permissions_ids
                    permission_dict[model_name]['delete'] = permission.id
                elif permission.codename == f'view_{model_name}':
                    permission_dict[model_name]['isView'] = permission.id in group_permissions_ids
                    permission_dict[model_name]['view'] = permission.id

            # Convert dictionary to a list
            permission_data = list(permission_dict.values())

            return Response({
                'status': True,
                'message': 'Permission List!',
                'data': permission_data
            })
        except Exception as e:
            return Response({"status": False,"message": str(e),"data":[]})



class CreateGroupWithPermissionViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


    def create(self, request, *args, **kwargs):
        try:
            name = request.data.get('name')
            permissions = request.data.get('permissions',[])

            if not name:
                return Response({"status": False,'message': 'Group name is required','data':[]})
            if not permissions:
                return Response({"status": False,'message': 'Permissions is required','data':[]})
            
            group = Group.objects.create(name = name)
            for permission in permissions:
                group.permissions.add(permission)
            group.save()
            serializer = GroupSerializer(group)
            data = serializer.data
            return Response({"status": True, "message": "Group created successfully!", "data": data})
        except Exception as e:
            return Response({"status": False,"message": str(e),"data":[]})
        
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            if queryset.exists():
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = GroupSerializer(page, many=True)
                    serializer = self.get_paginated_response(serializer.data)
                else:
                    serializer = GroupSerializer(queryset, many=True)
                count = serializer.data['count']
                limit = int(request.GET.get('page_size', 10))
                return Response({"status": True, "message":"Group List Successfully", 
                                'total_page': (count + limit - 1) // limit,
                                'count':count,
                                'data': serializer.data['results']})
            else:
                return Response({"status": False,"message":"No data found!","data":[]})
        except Exception as e:
            return Response({"status": False,"message": str(e),"data":[]})

class UpdateGroupWithPermissionViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def update(self, request, *args, **kwargs):
        try:
            group_id = kwargs.get('group_id')
            name = request.data.get('name')
            permissions = request.data.get('permissions',[])

            if not group_id:
                return Response({"status": False,'message': 'Group id is required','data':[]})
            if not name:
                return Response({"status": False,'message': 'Group name is required','data':[]})
            if not permissions:
                return Response({"status": False,'message': 'Permissions is required','data':[]})
            
            group = Group.objects.filter(id = group_id).first()   # get group by id
            if not group:
                return Response({"status": False,"message": "Group not found!","data":[]})
            group.name = name   # update group name
            group.permissions.clear()  # remove all permissions from group
            for permission in permissions:
                group.permissions.add(permission)  # add new permissions to group
            group.save()
            serializer = GroupSerializer(group)
            data = serializer.data
            return Response({"status": True, "message": "Group updated successfully!", "data": data})
        except Exception as e:
            return Response({"status": False,"message": str(e),"data":[]})
        

    def destroy(self, request, *args, **kwargs):
        # if group is assign to any user then it will not delete other wise it will delete
        try:
            group_id = kwargs.get('group_id')
            group = Group.objects.filter(id = group_id).first()
            if not group:
                return Response({"status": False,"message": "Group not found!","data":[]})
            if group.user_set.exists():  # check if group is assign to any user
                return Response({"status": False,"message": "This Group is assign to user, so it can not be deleted!","data":[]})
            group.delete()
            return Response({"status": True, "message": "Group deleted successfully!", "data": []})
        except Exception as e:
            return Response({"status": False,"message": str(e),"data":[]})
        


class CreateUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        try:
            email = request.data.get('email').lower()
            username = request.data.get('username')
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            phone = request.data.get('phone')
            department_id = request.data.get('department_id')
            group_ids  = request.data.get('user_role')

            
            if not email:
                return Response({"status": False, 'message': 'Email is required', 'data': []})
            if CustomUser.objects.filter(email=email).exists():
                return Response({"status": False, 'message': 'Email already exists', 'data': []})
            if CustomUser.objects.filter(username=username).exists():
                return Response({"status": False, 'message': 'Username already exists', 'data': []})
            if not username:
                return Response({"status": False, 'message': 'Username is required', 'data': []})
            if not department_id:
                return Response({"status": False, 'message': 'department is required', 'data': []})
            if not group_ids or not isinstance(group_ids, list):  # Check if it's a list
                return Response({"status": False, 'message': 'User roles must be a list of group IDs', 'data': []})
            
            groups = []
            for group_id in group_ids:
                try:
                    group = Group.objects.get(id=group_id)
                    groups.append(group)
                except Group.DoesNotExist:
                    return Response({"status": False, "message": "Invalid group ID: {group_id}", "data": []})
            
            try:
                department = Department.objects.get(id=department_id)
            except Department.DoesNotExist:
                return Response({"status": False, "message": "Invalid department ID", "data": []})

            # Use the imported function to generate a random password
            password = generate_random_password()

            user = CustomUser.objects.create(
                email=email,
                username=username,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                department = department
            )
            user.set_password(password)
            user.save()

            # Assign user to multiple groups
            for group in groups:
                user.groups.add(group)

            # Send email with username and password
            send_email_with_credentials(email, username, password, first_name)

            serializer = CustomUserSerializer(user,context={'request': request})
            data = serializer.data

            return Response({"status": True, "message": "User created successfully! Check your email for credentials.", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

class ListUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all().exclude(is_superuser = True).exclude(groups__name = "Admin").order_by('-id')
    serializer_class = CustomUserdataSerializer
    search_fields = ['email', 'username', 'first_name', 'last_name', 'phone']
    ordering_fields = ['email', 'username', 'first_name', 'last_name', 'phone']

    def get_queryset(self):
        user = self.request.user

        # Exclude Superadmin users from the queryset
        queryset = CustomUser.objects.all().exclude(is_superuser = True).exclude(groups__name = "Admin").order_by('-id')

        if user.groups.filter(name='Admin').exists():
            # Admin can see all data, including other Admin users
            return queryset
        else:
            # Other users can see all data except Admin and Superadmin users
            return queryset.exclude(groups__name='Admin')

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.serializer_class(queryset, many=True, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "User List Successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
        
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.models import Group

class UpdateUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def update(self, request, *args, **kwargs):
        try:
            user_id = kwargs.get('user_id')
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            phone = request.data.get('phone')
            is_active = request.data.get('is_active')
            groups = request.data.get('groups', [])
            is_dms_user = request.data.get('is_dms_user')
            
            if not user_id:
                return Response({"status": False, 'message': 'User ID is required', 'data': []})

            user = CustomUser.objects.filter(id=user_id).first()  # Get user by ID
            if not user:
                return Response({"status": False, "message": "User not found!", "data": []})

            # Update fields only if the value is not an empty string
            if first_name != "":
                user.first_name = first_name
            if last_name != "":
                user.last_name = last_name
            if phone != "":
                user.phone = phone
            if is_active is not None:
                if isinstance(is_active, str):
                    is_active = is_active.lower() in ('true', '1')
                user.is_active = is_active

            if is_dms_user is not None:
                if isinstance(is_dms_user, str):
                    is_dms_user = is_dms_user.lower() in ('true', '1')
                user.is_dms_user = is_dms_user

            # Update groups and permissions only if groups list is not empty
            if groups is not None:
                if groups:  # Check if groups list is not empty
                    user.groups.clear()
                    user.user_permissions.clear()

                    for group_id in groups:
                        try:
                            group = Group.objects.get(id=group_id)
                            user.groups.add(group)

                            for permission in group.permissions.all():
                                user.user_permissions.add(permission)

                        except Group.DoesNotExist:
                            return Response({"status": False, "message": f"Group with ID {group_id} does not exist!", "data": []})

            user.save()
            serializer = CustomUserSerializer(user,context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "User updated successfully!", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})


# class LoginAPIView(viewsets.ModelViewSet):
#     def create(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.validated_data
#             if not user.is_reset_password:
#                 user.increment_login_count()
#                 if user.login_count >= 3:
#                     return Response({"status": False,"message": "Your account is blocked.", "data": []})
#             login(request, user)
#             refresh = RefreshToken.for_user(user)
#             serializer = CustomUserSerializer(user,context={'request': request})
#             data = serializer.data
#             data['token'] = str(refresh.access_token)
#             return Response({"message": "Login successfully", "data": data})
#         return Response({"status": False,"message": "Invalid credentials", "data": []})

class LoginAPIView(viewsets.ViewSet):
    def create(self, request):
        try:
            username = request.data.get('username', '').strip()
            password = request.data.get('password', '').strip()
            group_id = request.data.get('group_id', None)

            if not username:
                return Response({"status": False, 'message': 'Username is required', "data": []})
            if not password:
                return Response({"status": False, 'message': 'Password is required', "data": []})
            if not group_id:
                return Response({"status": False, 'message': 'Group ID is required', "data": []})

            user = CustomUser.objects.filter(username=username).first()
            if not user:
                return Response({"status": False, "message": "Invalid username or password!", "data": []})

            if not user.is_active:
                return Response({"status": False, "message": "Your account is blocked. Please contact support.", "data": []})

            if user.is_password_expired():
                return Response({"status": False, "message": "Your password has expired. Please reset it.", "data": [], "is_password_expired": True})

            if not user.groups.filter(id=group_id).exists():
                return Response({"status": False, "message": "Invalid group ID.", "data": []})

            if not user.groups.filter(id=group_id).exists():
                return Response({"status": False, "message": "Invalid group ID.", "data": []})

            user_auth = authenticate(username=username, password=password)
            if not user_auth:
                # Increment failed login count
                user.login_count += 1
                user.save()

                if user.login_count >= 3:
                    user.is_blocked = True
                    user.save()
                    return Response({"status": False, "message": "Your account is blocked.", "data": []})

                return Response({"status": False, "message": "Invalid username or password!", "data": []})

            # Reset failed login count and log in user
            user.login_count = 0
            user.is_login = True
            user.save()

            refresh = RefreshToken.for_user(user_auth)
            serializer = LoginUserSerializer(user_auth, context={'request': request})
            data = serializer.data
            data['token'] = str(refresh.access_token)
            return Response({"status": True, "message": "You are logged in!", "data": data})
        
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Login error: {str(e)}", exc_info=True)
            return Response({"status": False, 'message': "Something went wrong!", 'data': []})

class ResetPasswordAPIView(viewsets.ModelViewSet):
    def update(self, request):
        user = self.request.user
        if user.is_anonymous:
            return Response({"status": False, "message": "User is not authenticated", "data": []})

        old_password = request.data.get('old_password')

        if not check_password(old_password, user.password):
            return Response({"status": False, "message": "Old password is incorrect", "data": []})

        try:
            otp = str(random.randint(100000, 999999))
            user.otp = otp
            user.save()

            return Response({"status": True,"message": "Otp genrate successfully", "data": []})
        except CustomUser.DoesNotExist:
            return Response({"status": False,"message": "User not found", "data": []})

class ConfirmOTPAndSetPassword(viewsets.ModelViewSet):
    def update(self, request):
        user = request.user
        if user.is_anonymous:
            return Response({"status": False, "message": "User is not authenticated", "data": []})

        otp = request.data.get('otp')
        new_password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if not otp or not new_password or not confirm_password:
            return Response({"status": False, "message": "OTP, new password, and confirm password are required", "data": []})

        if otp != user.otp:
            return Response({"status": False, "message": "Invalid OTP", "data": []})

        if new_password != confirm_password:
            return Response({"status": False, "message": "Password and confirm password do not match", "data": []})

        if check_password(new_password, user.old_password):
            return Response({"status": False, "message": "New password cannot be the same as the old password", "data": []})

        user.old_password = new_password
        user.password = make_password(new_password)
        user.password_updated_at = now()
        user.otp = None  
        user.is_reset_password = True
        user.login_count = 0
        user.save()

        return Response({"status": True, "message": "Password reset successfully", "data": []})

class RequestOTPViewSet(viewsets.ModelViewSet):
    def create(self, request):
        email = request.data.get('email')
        
        if not email:
            return Response({"status": False, "message": "Email is required", "data": []})
        
        try:
            user = CustomUser.objects.get(email=email)
            otp = str(random.randint(100000, 999999))
            user.otp = otp
            user.save()
            first_name = user.first_name    
            send_email_forgot_password(email, first_name, otp)

            return Response({"status": True, "message": "OTP sent to your email", "data": []})
        except CustomUser.DoesNotExist:
            return Response({"status": False, "message": "User not found", "data": []})


class VerifyOTPAndResetPasswordViewSet(viewsets.ModelViewSet):
    def create(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        
        if not email or not otp or not password or not confirm_password:
            return Response({"status": False, "message": "All fields are required", "data": []})
        
        if password != confirm_password:
            return Response({"status": False, "message": "Password and confirm password do not match", "data": []})

        try:
            user = CustomUser.objects.get(email=email)

            if user.otp != otp:
                return Response({"status": False, "message": "Invalid OTP", "data": []})

            user.password = make_password(password)
            user.is_reset_password = True
            user.otp = None
            user.save()
            
            return Response({"status": True, "message": "Password reset successfully", "data": []})
        except CustomUser.DoesNotExist:
            return Response({"status": False, "message": "User not found", "data": []})



class AdminResetLoginCountAPIView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    lookup_field = 'user_id' 
    # if we want to give admin so give that

    def update(self, request, *args, **kwargs):
        user_id = self.kwargs.get("user_id")
        password = request.data.get('password')

        if not CustomUser.objects.filter(id = user_id).exists():
                return Response({"status": False,'message': 'User not found','data':[]})

        if not password:
            return Response({"status": False,"message": "password are required", "data": []})
        try:
            user = CustomUser.objects.get(id = user_id)
            user.password = make_password(password)
            user.is_reset_password = True
            user.login_count = 0  # Reset login count on password reset
            user.save()
            return Response({"status": True,"message": "Password reset successfully", "data": []})
        except CustomUser.DoesNotExist:
            return Response({"status": False,"message": "User not found", "data": []})
        

class ListUserGroupsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        try:
            queryset = Group.objects.all().order_by('name') 
            serializer = GroupSerializer(queryset, many=True)
            data = serializer.data
            return Response({"status": True, "message": "User Groups List Successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
            
class EsignatureViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request):
        try:
            if not self.request.user.is_authenticated:
                return Response({"status": False, "message": "User not authenticated."})
            
            password = request.data.get('password')

            if not password:
                return Response({"status": False, "message": "Password is required."})

            if self.request.user.check_password(password):
                return Response({"status": True, "message": "Your password is correct."})
            else:
                return Response({"status": False, "message": "Incorrect password."})

        except Exception as e:
            return Response({"status": False, "message": f"An error occurred: {str(e)}"})
        
class SwitchRoleViewSet(viewsets.ModelViewSet):
    def create(self, request):
        user = request.user
        group_name = request.data.get('group_name')
        password = request.data.get('password')

        if not group_name or not password:
            return Response({"status": False, "message": "Group name and password are required", "data": []})

        if not user.check_password(password):
            return Response({"status": False, "message": "Incorrect password", "data": []})

        try:
            group = Group.objects.get(name=group_name)
            if not user.groups.filter(id=group.id).exists():
                return Response({"status": False, "message": "User is not part of the requested group", "data": []})
        except Group.DoesNotExist:
            return Response({"status": False, "message": "Group not found", "data": []})

        serializer = GroupPermissionSerializer(group)

        return Response({"status": True, "message": "Permissions retrieved successfully", "data": serializer.data})


class ListRequestUserGroupsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        try:
            user = request.user  # Get the logged-in user
            queryset = user.groups.all().order_by('name')  # Fetch only the user's groups
            serializer = GroupSerializer(queryset, many=True)
            data = serializer.data
            return Response({
                "status": True,
                "message": "User Groups List Retrieved Successfully",
                "data": data
            })
        except Exception as e:
            return Response({
                "status": False,
                "message": str(e),
                "data": []
            })
        

class UserGroupDropdownViewSet(viewsets.ModelViewSet):

    queryset = Group.objects.none()
    serializer_class = GroupSerializer

    def create(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is not None:
            # User authenticated, fetch groups
            groups = user.groups.all().order_by('name')
            serializer = self.get_serializer(groups, many=True)

            # Add the user's first name to the response
            return Response({
                "status": True,
                "message": "User Groups List Retrieved Successfully",
                "data": {
                    "user_first_name": user.first_name,
                    "groups": serializer.data
                }
            })
        else:
            # Authentication failed
            return Response({
                "status": False,
                "message": "Invalid username or password",
                "data": []
            })

class SwitchRoleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    def create(self, request):
        user = request.user
        group_id = request.data.get('group_id')
        password = request.data.get('password')

        # Validate input
        if not group_id or not password:
            return Response({"status": False, "message": "Group ID and password are required", "data": []})

        if not user.check_password(password):
            return Response({"status": False, "message": "Incorrect password", "data": []})

        try:
            # Fetch the group using group_id
            group = Group.objects.get(id=group_id)
            if not user.groups.filter(id=group.id).exists():
                return Response({"status": False, "message": "User is not part of the requested group", "data": []})
        except Group.DoesNotExist:
            return Response({"status": False, "message": "Group not found", "data": []})

        # Serialize the group and permissions
        serializer = GroupPermissionSerializer(group)

        return Response({"status": True, "message": "Permissions retrieved successfully", "data": serializer.data})



class CreateReminderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            reminder_minutes = request.data.get('reminder_minutes',[])
            if not reminder_minutes:
                return Response({"status": False, "message": "Reminder minutes are required", "data": []})

            user = self.request.user
            reminder = Reminder.objects.create(user=user, reminder_minutes=reminder_minutes)
            serializer = ReminderSerializer(reminder)
            data = serializer.data

            return Response({"status": True, "message": "Reminder created successfully", "data": data})

        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
    def list(self, request, *args, **kwargs):
        try:
            reminders = Reminder.objects.all()
            serializer = ReminderSerializer(reminders, many=True)
            data = serializer.data

            return Response({"status": True, "message": "Reminders fetched successfully", "data": data})

        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})


class ReviewerUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        try:
            # Get the "Reviewer" group
            reviewer_group = Group.objects.filter(name="Reviewer").first()
            if not reviewer_group:
                return Response({
                    "status": False,
                    "message": "Reviewer group does not exist",
                    "data": []
                })

            # Fetch users in the "Reviewer" group
            queryset = CustomUser.objects.filter(groups=reviewer_group).order_by('-id')

            # Serialize the data with MinimalUserSerializer
            serializer = MinimalUserSerializer(queryset, many=True, context={'request': request})
            data = serializer.data

            return Response({
                "status": True,
                "message": "Reviewer User List Retrieved Successfully",
                "data": data
            })
        except Exception as e:
            return Response({
                "status": False,
                "message": str(e),
                "data": []
            })