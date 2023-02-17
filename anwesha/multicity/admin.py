from django.contrib import admin
from .models import *
# from import_export.admin import ImportExportModelAdmin
# @admin.register(Multicity_Events)
class Events(admin.ModelAdmin):
    list_display = ("event_id","event_name","event_description","event_poster","event_date")
admin.site.register(Multicity_Events, Events)

@admin.register(Multicity_Participants)
class EventRegistration(admin.ModelAdmin):

    @admin.action(description='Lock Selected User')
    def lock_user(self, request, queryset):
        queryset.update(is_locked=True)
        self.message_user(request, "Selected User Locked")

    list_display= ("registration_id" , "event_id","leader_name","leader_email" , "solo_team")
    actions = [lock_user]
    list_filter = ('event_id','organisation_type','solo_team')
    fieldsets = (
        ('Leader Information' , {
            'fields' : (
                'leader_name',
                'leader_email',
                'leader_phone_no',
                'leader_organisation',
            )
        }),
        ('Member One Information' , {
            'fields' : (
                'member_one_name',
                'member_one_email',
                'member_one_phone_no',
                'member_one_organisation',
            )
        }),
         ('Member Two Information' , {
            'fields' : (
                'member_two_name',
                'member_two_email',
                'member_two_phone_no',
                'member_two_organisation',
            )
        }),
         ('Member Three Information' , {
            'fields' : (
                'member_three_name',
                'member_three_email',
                'member_three_phone_no',
                'member_three_organisation',
            )
        })
    )
    empty_value_display = '-empty-'
    search_fields = ['registration_id' , 'leader_name'  , 'leader_email']

