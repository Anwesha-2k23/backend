from django.contrib import admin
from .models import Sponsors
from utility import export_as_csv
@admin.register(Sponsors)
class SponsorsAdmin(admin.ModelAdmin):

    # custom action

    list_display = (
        'sponsor_name',
        'sponsor_phone_number',
        'sponsor_email',
    )
    actions = [export_as_csv]
    list_filter = ()
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'sponsor_name',
                'sponsor_phone_number',
                'sponsor_email',
                'sponsor_logo',
            )
        }),
        ('Social Links', {
            'fields': (
                ('sponsor_link', 'sponsor_instagram_id'),
                ('sponsor_facebook_id', 'sponsor_linkdin_id')
            )
        }),
    )
    empty_value_display = '-empty-'
    search_fields = [
        'sponsor_name',
        'sponsor_phone_number',
        'sponsor_email',
    ]
