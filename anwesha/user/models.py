from distutils.command import upload
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

# Determine storage settings based on the configuration
if CONFIGURATION == "local":
    QrStorageSettings = models.ImageField(blank=True, null=True, upload_to="static/qr")
    ProfilePhotoStorageSettings = models.ImageField(blank=True, null=True, upload_to="static/profile")
elif CONFIGURATION == "production":
    QrStorageSettings = models.ImageField(storage=PublicQrStorage, blank=True, null=True)
    ProfilePhotoStorageSettings = models.ImageField(storage=ProfileImageStorage, blank=True, null=True)

class User(models.Model):
    """
    Model representing a User.

    Attributes:
        User_type_choice (Enum): Enum class for user types.
        Gender (Enum): Enum class for gender options.
        anwesha_id (str): Anwesha ID of the user.
        password (str): Hashed password of the user.
        phone_number (str): Phone number of the user.
        email_id (str): Email ID of the user.
        full_name (str): Full name of the user.
        collage_name (str): Name of the college of the user.
        age (int): Age of the user.
        is_email_verified (bool): Indicates if the user's email is verified or not.
        user_type (str): Type of the user (choices from User_type_choice).
        gender (str): Gender of the user (choices from Gender).
        accomadation_selected (bool): Indicates if the user has selected accommodation.
        is_profile_completed (bool): Indicates if the user has completed their profile.
        instagram_id (str): Instagram ID of the user.
        facebook_id (str): Facebook ID of the user.
        time_of_registration (datetime): Timestamp of user registration.
        is_locked (bool): Indicates if the user is locked.
        is_loggedin (bool): Indicates if the user is logged in.
        profile (ImageField): Image field for the user's profile.
        profile_photo (ImageField): Image field for the user's profile photo (storage settings based on configuration).
        qr_code (ImageField): Image field for the user's QR code (storage settings based on configuration).
        signature (str): Signature of the user.
        secret (str): Secret of the user.
    """

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
    profile_photo = ProfilePhotoStorageSettings
    qr_code = QrStorageSettings
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
            self.signature = hash_id(self.anwesha_id, self.secret)
            self.qr_code = generate_qr(self.signature)
        super(User, self).save(*args, **kwargs)
