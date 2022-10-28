from datetime import datetime
from random import choices
from time import clock_settime
from django.db import models
from user.models import User
from event.models import Events

# Create your models here.
class Participant(models.Model):

    anwesha_id              = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    event_id                = models.ForeignKey(Events, on_delete=models.CASCADE,blank=True,null=True)
    team_id                 = models.ForeignKey('Team', on_delete=models.CASCADE, blank=True, null=True)

class Team(models.Model):
    team_id                 = models.CharField(unique=True, max_length=10, primary_key=True)
    event_id                = models.ForeignKey(Events, on_delete=models.CASCADE)
    leader_id               = models.ForeignKey(User, on_delete=models.CASCADE)
    team_name               = models.CharField(max_length=100, blank=True, null=True)
    
class Payer(models.Model):
    team_id                 = models.ForeignKey('Team', on_delete=models.CASCADE, null=True)
    payer_id                = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_status          = models.CharField(max_length=10, choices=[('paid', 'paid'), ('unpaid', 'unpaid'), ('pending', 'pending')], default='unpaid')
    reference_id            = models.CharField(max_length=100)
    datetime                = models.DateTimeField(auto_now_add=True)