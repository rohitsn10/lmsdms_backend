from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager,AbstractUser
# from django.contrib.auth.models import Group
from .models import *
from django.core.validators import EmailValidator
import os
from django.utils.timezone import now


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The email field must be set')
        email = self.normalize_email(email)
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    
def get_timestamped_filename(instance, image):

    base, extension = os.path.splitext("image")
    timestamp = now().strftime('%Y%m%d%H%M%S')
    new_filename = f"{base}_{timestamp}{extension}"
    return os.path.join("profile_image", new_filename)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True,null=True, blank=True)    #email = models.EmailField(unique=True, validators=[EmailValidator(message="Invalid email address")])
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=5000, null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='profile_images/')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
   

    def get_full_name(self):
        return '{} {}'.format(self.email)

    def get_short_name(self):
        return self.email
