from django.db import models
from anwesha.storage_backend import MultiCityStorage

# Create your models here.

class City(models.Model):
    city_name = models.CharField(max_length=100)
    poster = models.ImageField(storage=MultiCityStorage, blank=True, null=True)
    venue = models.CharField(max_length=150)
    date = models.DateTimeField()
    contacts = models.JSONField()
    register_link = models.URLField()
    rulebook = models.URLField()
    description = models.TextField()
    events = models.JSONField()
