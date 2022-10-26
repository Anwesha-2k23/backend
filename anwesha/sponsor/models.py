from django.db import models

class Sponsors(models.Model):

    sponsor_name                    = models.CharField(max_length=50, unique=True)
    sponsor_phone_number            = models.CharField(max_length=13)
    sponsor_email                   = models.EmailField(unique= True)
    sponsor_logo                    = models.ImageField(blank=True , null=True , upload_to = 'static/sponsor_logo' )
    sponsor_link                    = models.URLField(null = True , blank = True)
    sponsor_instagram_id            = models.CharField(max_length=255,blank=True, null=True)
    sponsor_facebook_id             = models.CharField(max_length=255,blank=True, null=True)
    sponsor_linkdin_id              = models.CharField(max_length=255,blank=True, null=True)
    
    
    