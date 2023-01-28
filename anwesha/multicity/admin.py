from django.contrib import admin
from .models import *

# @admin.register(Multicity_Events)
class Events(admin.ModelAdmin):
    list_display = ("event_id","event_name","event_description","event_poster","event_date")

class EventRegistration(admin.ModelAdmin):
    list_display= ("event_id","organisation_type","leader_name","leader_email","leader_phone_no","leader_organisation","member_one_name","member_one_email","member_one_organisation","member_one_phone_no","member_two_name","member_two_email","member_two_organisation","member_two_phone_no","member_three_name","member_three_email","member_three_organisation","member_three_phone_no","registration_id")

admin.site.register(Multicity_Participants, EventRegistration)
admin.site.register(Multicity_Events, Events)