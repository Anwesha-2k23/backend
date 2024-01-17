from ctypes.wintypes import tagSIZE
from django.db import models
import datetime
from user.models import User
# Create your models here.
size = (
    ("1", "S"),
    ("2", "M"),
    ("3", "L"),
    ("4", "XL"),
    ("5", "XXL"),
    ("6", "XXXL"),
)

class add_merch(models.Model):
    title= models.CharField(max_length=30,primary_key=True)
    description= models.TextField(blank=True)
    prices= models.JSONField()
    size= models.CharField(max_length=50, choices=size)
    image= models.ImageField(upload_to="static/merch/", default=None)

class order_merch(models.Model):
    merch_title= models.ForeignKey(add_merch, on_delete=models.CASCADE)
    name= models.CharField(max_length=30)
    email= models.EmailField(max_length=100)
    phone_no= models.CharField(max_length=13)
    address= models.TextField(max_length=200)
    size= models.CharField(max_length=50, choices=size)
    quantity= models.IntegerField(default=0)
    payment_status= models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=datetime.datetime.now)