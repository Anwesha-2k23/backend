from email.policy import default
from enum import Enum, unique
from hashlib import blake2b
from re import T
from secrets import choice
from django.db import models
from anwesha.storage_backend import ProfileImageStorage, PublicQrStorage
from anwesha.settings import CONFIGURATION
from utility import generate_qr, createId, hashpassword, hash_id
from django.core.files.storage import FileSystemStorage

'''
:NOTE:
While hosting images in S3 `QrStorageSettings` and `ProfilePhotoStorageSettings` needs to be changed accodingly

use following :CODE:

QrStorageSettings = models.ImageField(storage=PublicQrStorage, blank=True, null=True)
ProfilePhotoStorageSettings = models.ImageField(storage=ProfileImageStorage, blank=True, null=True)
'''

class User(models.Model):

    class User_type_choice(models.TextChoices):
        IITP_STUDENT = "iitp_student", "IITP-Student"
        STUDENT = "student", "Student"
        NON_STUDENT = "non-student", "Non-Student"
        ALUMNI = "alumni", "Alumni"
        GUEST = "guest", "Guest"

    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"
        OTHERS = "others", "Others"
        RATHER_NOT_SAY = "rather_not_say", "Rather not say"

    anwesha_id = models.CharField(max_length=10, primary_key=True, unique=True)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13, default="", unique=True, blank=True, null=True)
    email_id = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    collage_name = models.CharField(max_length=150, blank=True, null=True, default="IIT Patna")
    age = models.SmallIntegerField(blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    user_type = models.CharField(
        max_length=20, choices=User_type_choice.choices, blank=True, null=True, default=User_type_choice.STUDENT
    )
    gender = models.CharField(
        max_length=20, choices=Gender.choices, blank=True, null=True
    )
    accomadation_selected = models.BooleanField(default=False)
    is_profile_completed = models.BooleanField(default=False)
    instagram_id = models.CharField(max_length=255, blank=True, null=True)
    facebook_id = models.CharField(max_length=255, blank=True, null=True)
    time_of_registration = models.DateTimeField(auto_now_add=True)
    is_locked = models.BooleanField(default=False)
    is_loggedin = models.BooleanField(default=False)
    profile = models.ImageField()
    # profile_photo = models.ImageField(blank=True, null=True, upload_to="static/profile")
    profile_photo = models.ImageField(blank=True,null=True,storage=ProfileImageStorage)
    
    # qr_code = models.ImageField(blank=True, null=True, upload_to="static/qr")
    qr_code = models.ImageField(blank=True,null=True,storage=PublicQrStorage)
    
    signature = models.CharField(max_length=200, blank=True, null=True, default="signature")
    secret = models.CharField(max_length=20, default="secret")

    def __str__(self):
        """
        Returns the string representation of the user.
        """
        return self.anwesha_id

    def meta(self):
        """
        Returns the metadata of the user.
        """
        verbose_name = "User"
        verbose_name_plural = "Users"

    def save(self, *args, **kwargs):
        """
        Saves the user instance.

        - If the QR code is not set, generates a unique Anwesha ID, hashes the password, and generates a QR code.
        - If the Anwesha ID already exists, generates a new unique Anwesha ID.
        """
        if not self.qr_code:
            self.anwesha_id = createId("ANW", 7)
            check_exist = User.objects.filter(anwesha_id=self.anwesha_id)
            while check_exist:  # very unlikely to happen
                self.anwesha_id = createId("ANW", 7)
                check_exist = User.objects.filter(anwesha_id=self.anwesha_id)
            self.password = hashpassword(self.password)
            self.secret = createId("secret", 10)
            # Made changes in the QR file name in the generate_qr function so that no unnecessary folders are created during saving the QR code.
            self.signature = hash_id(self.anwesha_id, self.secret)
            self.qr_code = generate_qr(self.anwesha_id,self.signature)
        super(User, self).save(*args, **kwargs)
