from django.db import models
from user.models import User
from event.models import Events

class Payments(models.Model):
    EVENT_TYPE_CHOICES = [
        ('solo', 'Solo'),
        ('team', 'Team'),
    ]

    anwesha_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registrations')
    email_id = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    event_id = models.ForeignKey(Events, on_delete=models.CASCADE, related_name='registrations')
    event_type = models.CharField(max_length=10, choices=EVENT_TYPE_CHOICES, default='solo')
    atompay_transaction_id = models.CharField(max_length=100)
    bank_transaction_id = models.CharField(max_length=100)

    class Meta:
        unique_together = ('anwesha_id', 'event_id', 'event_type')
        verbose_name = 'Event Registration'
        verbose_name_plural = 'Event Registrations'

    def __str__(self):
        return f"{self.anwesha_id} - {self.event_id} ({self.event_type})"
