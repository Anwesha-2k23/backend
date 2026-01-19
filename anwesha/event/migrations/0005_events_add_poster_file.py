# Generated migration for adding poster_file field to Events model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_soloparicipants_has_entered_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='poster_file',
            field=models.ImageField(blank=True, null=True, upload_to='static/event_posters/'),
        ),
    ]
