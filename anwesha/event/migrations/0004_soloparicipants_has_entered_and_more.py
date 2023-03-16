# Generated by Django 4.1.5 on 2023-03-16 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_payutxn_is_processed'),
    ]

    operations = [
        migrations.AddField(
            model_name='soloparicipants',
            name='has_entered',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='teamparticipant',
            name='has_entered',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
