from ctypes.wintypes import tagSIZE
from django.db import models
import datetime

###  Code for TAGS  ###
# Add your Event Tags here
TAGS = (
    ("1", "tech"),
    ("2", "cultural"),
    ("3", "sports"),
    ("4", "gaming"),
    ("5", "workshop"),
    ("6", "other"),
)

tag_dict = {
    "tech": "1",
    "cultural": "2",
    "sports": "3",
    "gaming": "4",
    "workshop": "5",
    "other": "6",
}
### Code for TAGS ends here ###


class Events(models.Model):

    # enum for type
    id = models.CharField(unique=True, max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    organizer = models.CharField(max_length=100)
    venue = models.CharField(max_length=255)
    start_time = models.DateTimeField(blank=True)
    description = models.TextField()
    end_time = models.DateTimeField(blank=True)
    prize = models.CharField(max_length=150)
    registration_fee = models.DecimalField(max_digits=8, decimal_places=2 , default=0)
    video = models.URLField(blank=True)
    max_team_size = models.SmallIntegerField()
    registration_deadline = models.DateTimeField(blank=True)
    poster = models.URLField(blank=True)
    tags = models.CharField(max_length=40, choices=TAGS, blank=True)
    min_team_size = models.SmallIntegerField()
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['start_time']
        verbose_name = "Event"
        verbose_name_plural = "Events"


class Gallery(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to="static/gallery/", default=None)
    type = models.CharField(
        max_length=10, choices=(("1", "image"), ("2", "video")), default="1"
    )
    tags = models.CharField(max_length=40, choices=TAGS, blank=True)
    timestamp = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Gallery"
        verbose_name_plural = "Gallery"