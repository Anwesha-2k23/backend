from django.db import models
from user.models import User
from datetime import datetime   
# from anwesha.storage_backend import ProfileImageStorage
from anwesha.settings import CONFIGURATION
from time import timezone
class Campus_ambassador(models.Model):
    class ambassador_intrests(models.TextChoices):
        INTREST1 = 'intrest1', 'Intrest 1'
        INTREST2 = 'intrest2', 'Intrest 2'
        INTREST3 = 'intrest3', 'Intrest 3'
        
    class Gender(models.TextChoices):
        MALE = 'male' , 'Male'
        FEMALE = 'female' , 'Female'
        OTHERS = 'others' , 'Others'
        RATHER_NOT_SAY = 'rather_not_say' , 'Rather not say'
    ca_id                   = models.CharField(max_length=10 ,unique=True,primary_key=True,default='x')
    anwesha                 = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    password                = models.CharField(max_length=100)
    phone_number            = models.CharField(max_length=13)
    email_id                = models.EmailField(unique= True)
    full_name               = models.CharField(max_length=100)
    college_name            = models.CharField(max_length=150 , blank=True, null=True , default="IIT Patna")
    college_city            = models.CharField(max_length=150 , blank=True, null=True , default= "Patna")
    refferal_code           = models.CharField(max_length=150 , blank=True, null=True) 
    age                     = models.SmallIntegerField(blank=True , null=True , default=19)
    intrests                = models.CharField(max_length=150 , choices=ambassador_intrests.choices , blank = True , null = True)
    gender                  = models.CharField(max_length=20 , choices =Gender.choices , default=Gender.RATHER_NOT_SAY)
    score                   = models.IntegerField(default = 0)
    is_loggedin             = models.BooleanField(default=False)
    validation              = models.BooleanField(default=False)
    instagram_id            = models.CharField(max_length=255,blank=True, null=True)
    facebook_id             = models.CharField(max_length=255,blank=True, null=True)
    linkdin_id              = models.CharField(max_length=255,blank=True, null=True)
    twitter_id              = models.CharField(max_length=255,blank=True, null=True)
    date_of_birth           = models.DateTimeField(blank=True, null=True)
    time_of_registration    = models.DateTimeField(auto_now_add=True)
    profile_photo           = models.ImageField(blank=True , null=True , upload_to='profile')
    # profile_photo           = models.ImageField(blank=True , null=True ,storage=ProfileImageStorage)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name_plural = "Campus Ambassadors"
        verbose_name = "Campus Ambassador"
