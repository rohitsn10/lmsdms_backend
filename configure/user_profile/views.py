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


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    lookup_url_kwarg = 'pk'
    

class GroupIdWisePermissionListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    # filterset_class = PermissionFilter
   
    def get(self, request):
        if not request.user.has_perm('auth.view_permission'):
            return Response({'status': False, 'message': "You don't have permission to perform this action"})

        group_id = int(request.GET.get('group_id', None))
        user = request.user

        group_permissions_ids = []
        if group_id is not None:
            try:
                group = Group.objects.get(id=group_id)
                group_permissions_ids = group.permissions.values_list('id', flat=True)
            except Group.DoesNotExist:
                return Response({'status': False, 'message': 'Group not found!'})

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


class PermissionListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            if not request.user.has_perm('auth.view_permission'):
                return Response({'status': False, 'message': "You don't have permission to perform this action"})

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
            email = request.data.get('email')
            username = request.data.get('username')
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            phone = request.data.get('phone')
            
            if not email:
                return Response({"status": False, 'message': 'Email is required', 'data': []})
            if not username:
                return Response({"status": False, 'message': 'Username is required', 'data': []})

            # Use the imported function to generate a random password
            password = generate_random_password()

            user = CustomUser.objects.create(
                email=email,
                username=username,
                first_name=first_name,
                last_name=last_name,
                phone=phone
            )
            user.set_password(password)
            user.save()

            # Send email with username and password
            send_mail(
                'Your account has been created',
                f'Username: {username}\nPassword: {password}',
                'kalpesh.g@n10tech.com',  # Replace with your sender email
                [email],
                fail_silently=False,
            )

            serializer = CustomUserSerializer(user)
            data = serializer.data

            return Response({"status": True, "message": "User created successfully! Check your email for credentials.", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

class ListUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    search_fields = ['email','username','first_name','last_name','phone']
    ordering_fields = ['email','username','first_name','last_name','phone']

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            if queryset.exists():
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = CustomUserSerializer(page, many=True)
                    serializer = self.get_paginated_response(serializer.data)
                else:
                    serializer = CustomUserSerializer(queryset, many=True)
                count = serializer.data['count']
                limit = int(request.GET.get('page_size', 10))
                return Response({"status": True, "message": "User List Successfully", 
                                'total_page': (count + limit - 1) // limit,
                                'count':count,
                                'data': serializer.data['results']})
            else:
                return Response({"status": False,"message":"No data found!","data":[]})
        except Exception as e:
            return Response({"status": False,"message": str(e),"data":[]})

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
            if not user_id:
                return Response({"status": False, 'message': 'User ID is required', 'data': []})

            user = CustomUser.objects.filter(id=user_id).first()  # Get user by ID
            if not user:
                return Response({"status": False, "message": "User not found!", "data": []})

            if first_name is not None:
                user.first_name = first_name
            if last_name is not None:
                user.last_name = last_name
            if phone is not None:
                user.phone = phone
            if is_active is not None:
                if isinstance(is_active, str):
                    is_active = is_active.lower() in ('true', '1')
                user.is_active = is_active

            user.save()
            serializer = CustomUserSerializer(user)
            data = serializer.data
            return Response({"status": True, "message": "User updated successfully!", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})

        

class LoginAPIView(viewsets.ModelViewSet):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            if not user.is_reset_password:
                user.increment_login_count()
                if user.login_count >= 3:
                    return Response({"message": "Your account is blocked."}, status=status.HTTP_403_FORBIDDEN)
            return Response({"message": "Login successful"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordAPIView(viewsets.ModelViewSet):
    def post(self, request):
        username = request.data.get('username')
        try:
            user = CustomUser.objects.get(username=username)
            user.is_reset_password = True
            user.login_count = 0  # Reset login count on password reset
            user.save()
            return Response({"message": "Password reset successful"})
        except CustomUser.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class AdminResetLoginCountAPIView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]  
    # if we want to give admin so give that

    def post(self, request):
        username = request.data.get('username')
        try:
            user = CustomUser.objects.get(username=username)
            serializer = ResetLoginCountSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.reset_login_count()
                return Response({"message": "Login count reset successful"})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            