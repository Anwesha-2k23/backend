from distutils.command import upload
from email.policy import default
from enum import Enum, unique
from hashlib import blake2b
from re import T
from secrets import choice
from django.db import models

class User(models.Model):
    class User_type_choice(models.TextChoices):
        STUDENT = 'student', 'Student'
        NON_STUDENT = 'non-student', 'Non-Student'
        ALUMNI = 'alumni', 'Alumni'
    
    class Gender(models.TextChoices):
        MALE = 'male' , 'Male'
        FEMALE = 'female' , 'Female'
        OTHERS = 'others' , 'Others'
        RATHER_NOT_SAY = 'rather_not_say' , 'Rather not say'

    

    anwesha_id              = models.CharField(max_length=10, primary_key=True, unique=True)
    password                = models.CharField(max_length=100)
    phone_number            = models.CharField(max_length=13)
    email_id                = models.EmailField(unique= True)
    full_name               = models.CharField(max_length=100)
    college_name            = models.CharField(max_length=150 , blank=True, null=True)
    profile_photo           = models.ImageField(blank=True , null=True , upload_to = 'static/profile_photo' , default = 'static/images.jpeg')
    age                     = models.SmallIntegerField(blank=True , null=True)
    is_email_verified       = models.BooleanField(default=False)
    user_type               = models.CharField(max_length=11 , choices=User_type_choice.choices , blank = True , null = True)
    qr_code                 = models.ImageField(blank=True , null=True , upload_to = 'static/qrcode')
    gender                  = models.CharField(max_length=20 , choices =Gender.choices , blank=True, null=True)
    accomadation_selected   = models.BooleanField(default=False)
    is_profile_completed    = models.BooleanField(default=False)
    instagram_id            = models.CharField(max_length=255,blank=True, null=True)
    facebook_id             = models.CharField(max_length=255,blank=True, null=True)
    time_of_registration    = models.DateTimeField(auto_now_add=True)

