# Generated by Django 4.1.5 on 2025-01-25 22:15

import anwesha.storage_backend
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CA', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campus_ambassador',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, storage=anwesha.storage_backend.ProfileImageStorage, upload_to=''),
        ),
    ]
