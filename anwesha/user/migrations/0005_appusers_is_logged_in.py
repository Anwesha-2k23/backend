# Generated by Django 4.1.5 on 2025-01-31 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_appusers'),
    ]

    operations = [
        migrations.AddField(
            model_name='appusers',
            name='is_logged_in',
            field=models.BooleanField(default=False),
        ),
    ]
