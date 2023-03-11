from ctypes.wintypes import tagSIZE
from django.db import models
import datetime
from user.models import User
from utility import createId

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
size = (
    ("1", "S"),
    ("2", "M"),
    ("3", "L"),
    ("4", "XL"),
    ("5", "XXL"),
    ("6", "XXXL"),
)

class Events(models.Model):

    # enum for type
    id = models.CharField(unique=True, max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    organizer = models.CharField(max_length=100)
    venue = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    prize = models.CharField(max_length=150, default=0)
    registration_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    registration_deadline = models.DateTimeField(blank=True, null=True)
    video = models.URLField(blank=True)
    poster = models.URLField(blank=True)
    tags = models.CharField(max_length=40, choices=TAGS, blank=True)
    max_team_size = models.SmallIntegerField(default=1)
    min_team_size = models.SmallIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    is_online = models.BooleanField(default=False)
    registration_link = models.URLField(blank=True)
    order = models.IntegerField(default=0)
    payment_link = models.URLField(blank=True)
    payment_key = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['start_time']
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def save(self, *args, **kwargs):
        if not self.id or self.id == "":
            self.id = createId("EVT", 5)
        super(Events, self).save(*args, **kwargs)


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

class add_merch(models.Model):
    title= models.CharField(max_length=30,primary_key=True)
    description= models.TextField(blank=True)
    prices= models.JSONField()
    # size= models.CharField(max_length=50)
    image= models.ImageField(upload_to="static/merch/", default=None)
    payment_link=models.CharField(max_length=200,null=True,blank=True)

class order_merch(models.Model):
    merch_title= models.ForeignKey(add_merch, on_delete=models.CASCADE)
    anwesha_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    address= models.TextField(max_length=200)
    size= models.CharField(max_length=50, choices=size,null=True,blank=True)
    transaction_id=models.CharField(max_length=100,null=True,blank=True)
    payment_done = models.BooleanField(default=False)
    order_id = models.CharField(max_length=100,null=True,blank=True)
    quantity= models.IntegerField(default=0)
    payment_status= models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=datetime.datetime.now)

class TeamParticipant(models.Model):

    anwesha_id = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True
    )
    event_id = models.ForeignKey(
        Events, on_delete=models.CASCADE, blank=True, null=True
    )
    team_id = models.ForeignKey("Team", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.anwesha_id.anwesha_id


class Team(models.Model):
    
    team_id = models.CharField(unique=True, max_length=10, primary_key=True)
    event_id = models.ForeignKey(Events, on_delete=models.CASCADE )
    leader_id = models.ForeignKey(User, on_delete=models.CASCADE )
    team_name = models.CharField(max_length=100, blank=True, null=True)
    payment_done = models.BooleanField(default=False)
    txnid = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.team_name


class Payer(models.Model):
    class Payment_Status(models.TextChoices):
        PAID = "paid" ,"Paid"
        UNPAID = "unpaid", "Unpaid"
        PENDING = "pending", "Pending"
    team_id = models.ForeignKey("Team", on_delete=models.CASCADE, null=True, blank=True)
    payer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_status = models.CharField(
        max_length=10,
        choices=Payment_Status.choices,
        default=Payment_Status.UNPAID,
    )
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    order_id = models.CharField(max_length=100)
    signature = models.CharField(max_length=100)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payer_id.full_name

class SoloParicipants(models.Model):
    anwesha_id = models.ForeignKey( User, on_delete=models.CASCADE, blank=True, null=True)
    event_id = models.ForeignKey(Events, on_delete=models.CASCADE, blank=True, null=True)
    payment_done = models.BooleanField(default=False)
    order_id = models.CharField(max_length=100, blank=True, null=True)


class PayUTxn(models.Model):
    mihpayid = models.CharField(max_length=100, blank=True, null=True)
    mode = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    key = models.CharField(max_length=100, blank=True, null=True)
    txnid = models.CharField(max_length=100, blank=True, null=True)
    amount = models.CharField(max_length=100, blank=True, null=True)
    addedon = models.CharField(max_length=100, blank=True, null=True)
    productinfo = models.CharField(max_length=100, blank=True, null=True)
    firstname = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    field1 = models.CharField(max_length=100, blank=True, null=True)
    field2 = models.CharField(max_length=100, blank=True, null=True)
    field3 = models.CharField(max_length=100, blank=True, null=True)
    field4 = models.CharField(max_length=100, blank=True, null=True)
    field5 = models.CharField(max_length=100, blank=True, null=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return self.email
