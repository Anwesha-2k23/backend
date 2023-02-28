# Generated by Django 4.1.5 on 2023-02-22 18:24

import anwesha.storage_backend
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('qr_code', models.ImageField(blank=True, null=True, storage=anwesha.storage_backend.PublicQrStorage, upload_to='')),
                ('profile_photo', models.ImageField(blank=True, null=True, storage=anwesha.storage_backend.ProfileImageStorage, upload_to='')),
                ('anwesha_id', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('phone_number', models.CharField(blank=True, default='', max_length=13, null=True, unique=True)),
                ('email_id', models.EmailField(max_length=254, unique=True)),
                ('full_name', models.CharField(max_length=100)),
                ('collage_name', models.CharField(blank=True, max_length=150, null=True)),
                ('age', models.SmallIntegerField(blank=True, null=True)),
                ('is_email_verified', models.BooleanField(default=False)),
                ('user_type', models.CharField(blank=True, choices=[('iitp_student', 'IITP-Student'), ('student', 'Student'), ('non-student', 'Non-Student'), ('alumni', 'Alumni'), ('guest', 'Guest')], default='student', max_length=20, null=True)),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('others', 'Others'), ('rather_not_say', 'Rather not say')], max_length=20, null=True)),
                ('accomadation_selected', models.BooleanField(default=False)),
                ('is_profile_completed', models.BooleanField(default=False)),
                ('instagram_id', models.CharField(blank=True, max_length=255, null=True)),
                ('facebook_id', models.CharField(blank=True, max_length=255, null=True)),
                ('time_of_registration', models.DateTimeField(auto_now_add=True)),
                ('is_locked', models.BooleanField(default=False)),
                ('is_loggedin', models.BooleanField(default=False)),
                ('profile', models.ImageField(upload_to='')),
            ],
        ),
    ]
