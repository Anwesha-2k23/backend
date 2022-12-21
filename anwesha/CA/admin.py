from django.contrib import admin
from .models import Campus_ambassador

# Register your models here.
@admin.register(Campus_ambassador)
class Campus_ambassadorAdmin(admin.ModelAdmin):

    @admin.action(description='Incriment Score')
    def incriment_score(self, request, queryset):
        ca = queryset.get()
        queryset.update(score = ca.score + 1)
        self.message_user(request, "Score Incrimented")

    readonly_fields= ('time_of_registration',)
    list_display = (
        'full_name', 
        'college_name', 
        'email_id', 
        'phone_number',
        'score',
        )
    actions = [
        'incriment_score'
    ]
    list_filter = (
        'college_city',
        'score',
        'validation'
    )
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'anwesha',
                ('full_name', 'date_of_birth'),
                ('email_id', 'phone_number'),
                ('college_name', 'college_city'),
                'profile_photo',
                ('age', 'gender'),
                'intrests',
                ('score','refferal_code'),
            )
        }),
        ('Social Links', {
            'fields': (
                ('instagram_id','facebook_id'), 
                ('linkdin_id','twitter_id'),
                )
        }),
        ('Internal Flags', {
            'fields': (
                'time_of_registration',
                'validation',
            )
        }),
    )
    empty_value_display = '-empty-'
    search_fields = [
        'full_name',
        'college_name',
        'email_id',
        'phone_number',
        'college_city',
        'score',
    ]
