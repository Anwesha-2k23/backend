from django.db import models

class Multicity_Events(models.Model):
    event_id = models.CharField(max_length=4,unique=True)
    event_name = models.CharField(max_length=100,primary_key=True)
    event_description = models.TextField(default="description coming soon...")
    event_poster = models.ImageField(blank=True , null=True , upload_to='multicity_poster')
    event_date = models.DateTimeField(auto_now_add=True)

    class meta:
        verbose_name = "Multicity Event"
        verbose_name_plural = "Multicity Events"



class Multicity_Participants(models.Model):
    class Organisation_Type(models.TextChoices):
        SCHOOL = 'school' , 'School',
        COLLEGE = 'college' , 'College',
        OTHERS = 'other' , 'Other',
       
    registration_id = models.CharField(max_length=10 ,unique=True,primary_key=True)
    event_id = models.ForeignKey(Multicity_Events, on_delete=models.CASCADE)
    payment_done = models.BooleanField(default=False)
    organisation_type = models.CharField(max_length=20 , choices =Organisation_Type.choices , default=Organisation_Type.COLLEGE)
    solo_team = models.BooleanField(default=True)
    leader_name = models.CharField(max_length=100)
    leader_email = models.CharField(max_length=100)
    leader_phone_no = models.CharField(max_length=13)
    leader_organisation= models.CharField(max_length=100)
    member_one_name = models.CharField(max_length=100,blank=True,null=True,default=None)
    member_one_email = models.CharField(max_length=100,blank=True,null=True,default=None)
    member_one_organisation= models.CharField(max_length=100,blank=True,null=True,default=None)
    member_one_phone_no = models.CharField(max_length=13,blank=True,null=True,default=None)
    member_two_name = models.CharField(max_length=100,blank=True,null=True,default=None)
    member_two_email = models.CharField(max_length=100,blank=True,null=True,default=None)
    member_two_organisation= models.CharField(max_length=100,blank=True,null=True,default=None)
    member_two_phone_no = models.CharField(max_length=13,blank=True,null=True,default=None)
    member_three_name = models.CharField(max_length=100,blank=True,null=True,default=None)
    member_three_email = models.CharField(max_length=100,blank=True,null=True,default=None)
    member_three_organisation= models.CharField(max_length=100,blank=True,null=True,default=None)
    member_three_phone_no = models.CharField(max_length=13,blank=True,null=True,default=None)
    