from django.db import models
from user.models import User


class campus_ambassador(models.Model):
    class ambassador_intrests(models.TextChoices):
        INTREST1 = "intrest1", "Intrest 1"

    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"
        OTHERS = "others", "Others"
        RATHER_NOT_SAY = "rather_not_say", "Rather not say"

    anwesha_id = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True
    )
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13)
    email_id = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    college_name = models.CharField(max_length=150, blank=True, null=True)
    college_city = models.CharField(max_length=150, blank=True, null=True)
    college_state = models.CharField(max_length=150, blank=True, null=True)
    degree = models.CharField(max_length=150, blank=True, null=True)
    years_of_study = models.DateField()
    refferal_code = models.CharField(max_length=150, blank=True, null=True)
    profile_photo = models.ImageField(
        blank=True,
        null=True,
        upload_to="static/profile_photo",
        default="static/images.jpeg",
    )
    age = models.SmallIntegerField(blank=True, null=True)
    intrests = models.CharField(
        max_length=150, choices=ambassador_intrests.choices, blank=True, null=True
    )
    gender = models.CharField(
        max_length=20, choices=Gender.choices, blank=True, null=True
    )
    score = models.IntegerField(default=0)
    active = models.BooleanField(default=False)
    validation = models.BooleanField(default=False)
    instagram_id = models.CharField(max_length=255, blank=True, null=True)
    facebook_id = models.CharField(max_length=255, blank=True, null=True)
    linkdin_id = models.CharField(max_length=255, blank=True, null=True)
    twitter_id = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateTimeField()
    time_of_registration = models.DateTimeField(auto_now_add=True)
