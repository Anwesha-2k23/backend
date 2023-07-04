from django.db import models

# Sponsors Model Definition
class Sponsors(models.Model):
    # Fields to store sponsor information
    sponsor_name = models.CharField(max_length=50, unique=True)  # Name of the sponsor (Max 50 characters)

    sponsor_phone_number = models.CharField(max_length=15, unique=True)  # Phone number of the sponsor (Max 15 characters)

    sponsor_description = models.CharField(max_length=1000, blank=True, null=True)  # Description of the sponsor (optional)

    order = models.IntegerField(default=0)  # Order in which the sponsors are displayed (default: 0)

    sponsor_email = models.EmailField(unique=True)  # Email address of the sponsor (unique)

    sponsor_logo = models.ImageField(blank=True, null=True, upload_to="static/sponsor_logo")  # Sponsor's logo image

    sponsor_link = models.URLField(null=True, blank=True)  # Website link of the sponsor (optional)

    sponsor_instagram_id = models.CharField(max_length=255, blank=True, null=True)  # Instagram ID of the sponsor (optional)

    sponsor_facebook_id = models.CharField(max_length=255, blank=True, null=True)  # Facebook ID of the sponsor (optional)

    sponsor_linkdin_id = models.CharField(max_length=255, blank=True, null=True)  # LinkedIn ID of the sponsor (optional)

    def __str__(self):
        return self.sponsor_name

    class Meta:
        verbose_name_plural = "Sponsors"  # Plural name for the model in the admin interface
        verbose_name = "Sponsor"  # Singular name for the model in the admin interface
