from enum import Enum, unique
from django.db import models

class User(models.Model):
    class User_type_choice(models.TextChoices):
        STUDENT = 'student', 'Student'
        NON_STUDENT = 'non-student', 'Non-Student'
        ALUMNI = 'alumni', 'Alumni'

    anwesha_id              = models.CharField(max_length=10, primary_key=True, unique=True)
    password                = models.CharField(max_length=100, blank=True, null=True)
    phone_number            = models.CharField(max_length=13, blank=True, null=True)
    email_id                = models.EmailField(unique= True, blank=True, null=True)
    full_name               = models.CharField(max_length=100, blank=True, null=True)
    college_name            = models.CharField(max_length=150,blank=True,null=True)
    profile_photo           = models.URLField(blank=True , null=True)
    age                     = models.SmallIntegerField(blank=True, null=True)
    is_email_verified       = models.BooleanField(default=False, blank=True, null=True)
    user_type               = models.CharField(max_length=11 , choices=User_type_choice.choices, blank=True, null=True)
    qr_code                 = models.ImageField(blank=True , null=True)
    gender                  = models.CharField(max_length=20, blank=True, null=True)
    accomadation_selected   = models.BooleanField(default=False, blank=True, null=True)
    is_profile_completed    = models.BooleanField(default=False, blank=True, null=True)
    instagram_id            = models.CharField(max_length=255,blank=True, null=True)
    facebook_id             = models.CharField(max_length=255,blank=True, null=True)
    time_of_registration    = models.DateTimeField(auto_now_add=True, blank=True, null=True)

