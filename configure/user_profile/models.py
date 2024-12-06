from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager,AbstractUser
# from django.contrib.auth.models import Group
from .models import *
from django.core.validators import EmailValidator
import os
from django.utils.timezone import now
from django.conf import settings


class Department(models.Model):
    department_name = models.TextField()
    department_description = models.TextField()
    department_created_at = models.DateTimeField(auto_now_add=True)

class CustomUserManager(BaseUserManager):
    
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        # if not email:
        #     raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(username=username,email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)
    

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(null=True, blank=True)    #email = models.EmailField(unique=True, validators=[EmailValidator(message="Invalid email address")])
    username = models.CharField(max_length=255, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=5000, null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='profile_images/')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)
    department = models.ForeignKey(
        Department,  # String reference to avoid direct import
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )


    is_reset_password = models.BooleanField(default=False, null=True)
    login_count = models.IntegerField(default=0)

    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def get_full_name(self):
        return '{} {}'.format(self.email)

    def get_short_name(self):
        return self.email
    
    def increment_login_count(self):
        self.login_count += 1
        self.save()

    def reset_login_count(self):
        self.login_count = 0
        self.save()



class EmailTemplate(models.Model):
    name = models.CharField(max_length=500, unique=True)
    subject = models.CharField(max_length=500)
    content = models.TextField()
    from_email = models.EmailField(default=settings.EMAIL_HOST_USER)
    signature = models.CharField(max_length=255, default='Bharat Parenterals Ltd.')

    def __str__(self):
        return self.name
    
    
class Reminder(models.Model):
    reminder_minutes = models.JSONField(default=list)  # Stores a list of reminder minutes (e.g., [90, 60, 30, 15])

    def __str__(self):
        return f"Reminder Minutes: {', '.join(map(str, self.reminder_minutes))}"