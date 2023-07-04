from django.contrib import admin
from .models import Sponsors
from utility import export_as_csv

@admin.register(Sponsors)
class SponsorsAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Sponsors model.
    """

    # Custom action
    actions = [export_as_csv]

    # Displayed fields in the list view
    list_display = (
        'sponsor_name',
        'sponsor_phone_number',
        'sponsor_email',
    )

    # Filtering options in the list view
    list_filter = ()

    # Fieldsets to organize fields in the detail view
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'sponsor_name',
                'sponsor_description',
                'sponsor_phone_number',
                'sponsor_email',
                'sponsor_logo',
                'order',
            )
        }),
        ('Social Links', {
            'fields': (
                ('sponsor_link', 'sponsor_instagram_id'),
                ('sponsor_facebook_id', 'sponsor_linkdin_id')
            )
        }),
    )

    # Displayed value for empty fields
    empty_value_display = '-empty-'

    # Fields to search in the admin interface
    search_fields = [
        'sponsor_name',
        'sponsor_phone_number',
        'sponsor_email',
    ]
