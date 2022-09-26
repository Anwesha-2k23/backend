from django.db import models

class Events(models.Model) :

    #enum for type
    id                    = models.CharField(unique=True, max_length=10, primary_key=True)
    name                  = models.CharField(max_length=100)
    organizer             = models.CharField(max_length=100)
    venue                 = models.CharField(max_length=255)
    start_time            = models.DateTimeField(blank=True)
    description           = models.TextField()
    end_time              = models.DateTimeField(blank=True)
    prize                 = models.CharField(max_length=150)
    registration_fee      = models.DecimalField(max_digits=8, decimal_places=2)
    video                 = models.URLField(blank=True)
    max_team_size         = models.SmallIntegerField()
    registration_deadline = models.DateTimeField(blank=True)
    poster                = models.URLField(blank=True)