from django.contrib import admin
from .models import Campus_ambassador
from utility import export_as_csv
from django.db.models import F

@admin.register(Campus_ambassador)
class CAadmin(admin.ModelAdmin):

    @admin.action(description='Lock Selected User')
    def lock_user(self, request, queryset):
        queryset.update(is_locked=True)
        self.message_user(request, "Selected User Locked")

    @admin.action(description='score +5')
    def score5(self, request, queryset):
        queryset.update(score=F("score")+5)
        self.message_user(request, "Score incremented")
    
    @admin.action(description='score +10')
    def score10(self, request, queryset):
        queryset.update(score=F("score")+10)
        self.message_user(request, "Score incremented")
    
    @admin.action(description='score +15')
    def score15(self, request, queryset):
        queryset.update(score=F("score")+15)
        self.message_user(request, "Score incremented")
    
    list_display = ('ca_id', 'full_name', 'email_id', 'refferal_code','phone_number')
    actions = [lock_user,export_as_csv, score5, score10, score15]
    list_filter = ('college_name', 'college_city', 'intrests')
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'ca_id', 
                'full_name', 
                'email_id', 
                'phone_number',
                'profile_photo',
                'score',
                ('age', 'gender'),
                ('college_city' , 'college_name'),
            )
        }),
        ('Social Links', {
            'fields': ('instagram_id', 'facebook_id','linkdin_id', 'twitter_id')
        }),
        ('Internal Flags', {
            'fields': (('validation' ,'is_loggedin'), 'password')
        })
    )
    empty_value_display = '-empty-'
    search_fields = ['ca_id',  'email_id', 'full_name','phone_number', 'college_name']
