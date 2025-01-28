from django.db import models
from user.models import User


class FestPasses(models.Model):
    id = models.AutoField(primary_key=True)
    anwesha_id = models.OneToOneField(User, on_delete=models.CASCADE,unique=True)
    email_id = models.EmailField(unique=True)
    transaction_id = models.CharField(max_length=255,blank=False)    # AtompayTransactionID.
    has_entered = models.BooleanField(default=False)
    payment_done = models.BooleanField(default=False)
    
