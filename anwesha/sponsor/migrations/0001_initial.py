# Generated by Django 3.2.12 on 2022-10-22 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sponsors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sponsor_name', models.CharField(max_length=50, unique=True)),
                ('sponsor_phone_number', models.CharField(max_length=13)),
                ('sponsor_email', models.EmailField(max_length=254, unique=True)),
                ('sponsor_logo', models.ImageField(blank=True, null=True, upload_to='static/sponsor_logo')),
                ('sponsor_link', models.URLField(blank=True, null=True)),
                ('sponsor_instagram_id', models.CharField(blank=True, max_length=255, null=True)),
                ('sponsor_facebook_id', models.CharField(blank=True, max_length=255, null=True)),
                ('sponsor_linkdin_id', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]