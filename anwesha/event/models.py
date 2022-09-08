from django.db import models

class Events(models.Model) :

    #enum for type
    id                    = models.CharField(unique=True, max_length=10)
    name                  = models.CharField(max_length=100)
    organizer             = models.CharField(max_length=100)
    venue                 = models.CharField(max_length=255)
    start_time            = models.DateTimefield()
    description           = models.TextField()
    end_time              = models.DateTimeField()
    prize                 = models.CharField(max_length=150)
    registration_fee      = models.DecimalField(max_digits=8, decimal_places=2)
    video                 = models.URLField()
    max_team_size         = models.SmallIntegerField()
    registration_deadline = models.DateTimeField()
    poster                = models.URLField()

    class Meta:
        db_table = 'events'
