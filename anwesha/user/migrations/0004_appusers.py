# Generated by Django 4.1.5 on 2025-01-31 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_profile_photo_alter_user_qr_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppUsers',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('phone_number', models.CharField(max_length=10)),
                ('email_id', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
    ]
