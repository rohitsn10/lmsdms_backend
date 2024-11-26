from rest_framework import serializers
from .models import *
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import authenticate


class GroupSerializer(serializers.ModelSerializer):
    # permission_list = serializers.SerializerMethodField()
    permission_list = serializers.SerializerMethodField()
    class Meta:
        model = Group
        fields = ['id','name','permission_list']   # add 'permissions' if you want to see the permissions in the group

    def get_permission_list(self, obj):
        # Filter permissions that are assigned to the group
        permissions = obj.permissions.all().select_related('content_type')
        grouped_permissions = {}
        for permission in permissions:
            content_type = permission.content_type.model
            if content_type not in grouped_permissions:
                grouped_permissions[content_type] = {}
            action = permission.codename.split('_')[0]
            grouped_permissions[content_type][action] = permission.id
        
        permission_list = [{model: perms} for model, perms in grouped_permissions.items()]
        return permission_list

    # def get_permission_list(self, obj):
    #     permission_list = obj.permissions.all()
    #     return PermissionSerializer(permission_list, many=True).data

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id','name','content_type','codename',]


class CustomUserdataSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id','email','full_name','first_name','last_name','phone','username','created_at']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

class CustomUserSerializer(serializers.ModelSerializer):
    groups_list = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    user_permissions = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id','email','first_name','last_name','phone','department','is_active','is_staff','is_superuser','profile_image','groups_list','user_permissions','username', 'is_reset_password', 'login_count']

    def get_groups_list(self, obj):
        groups_data = [{'id': group.id, 'name': group.name} for group in obj.groups.all()]
        return groups_data if groups_data else None
    
    def get_user_permissions(self, obj):
        # Start with an empty dictionary to hold permission data grouped by content type
        permission_dict = {}
    
        # Iterate over all permissions assigned to the user
        for permission in obj.user_permissions.all().select_related('content_type'):
            model = permission.content_type.model  # Get the model name of the content type
    
            # Initialize the dictionary for this model, if not already done
            if model not in permission_dict:
                permission_dict[model] = {
                    "name": model,
                    "add": None,
                    "is_add": "false",
                    "change": None,
                    "is_change": "false",
                    "delete": None,
                    "is_delete": "false",
                    "view": None,
                    "is_view": "false"
                }
    
            # Extract the action (add, change, delete, view) from the permission codename
            action = permission.codename.split('_')[0]
            permission_dict[model]['permission_id'] = permission.id
            permission_dict[model][action] = permission.id
            permission_dict[model]["is_" + action] = "true"
    
        # Convert the dictionary to the list format you want
        user_permissions = list(permission_dict.values())
        return user_permissions if user_permissions else None


    def get_profile_image(self, obj):
        if obj.profile_image and hasattr(obj.profile_image, 'url'):
            request = self.context.get('request')
            return request.build_absolute_uri(obj.profile_image.url)
        return None
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            if user.login_count >= 3:
                raise serializers.ValidationError({"status": False,"message": "Your account is blocked.","data": []})
            return user
        else:
            raise serializers.ValidationError({"status": False,"message": "Invalid credentials","data": []})


class ResetLoginCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['login_count']

    def reset_login_count(self):
        self.instance.reset_login_count()
        return self.instance

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class GroupPermissionSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']

    def get_permissions(self, obj):
        # Get permissions for this group
        permissions = obj.permissions.all().select_related('content_type')
        permission_dict = {}

        for permission in permissions:
            model = permission.content_type.model
            if model not in permission_dict:
                permission_dict[model] = {
                    "name": model,
                    "add": None,
                    "is_add": "false",
                    "change": None,
                    "is_change": "false",
                    "delete": None,
                    "is_delete": "false",
                    "view": None,
                    "is_view": "false"
                }
            action = permission.codename.split('_')[0]
            permission_dict[model][action] = permission.id
            permission_dict[model]["is_" + action] = "true"
        
        return list(permission_dict.values()) if permission_dict else None
