from django.contrib import admin
from .models import Events, Gallery

# Register your models here.

# admin.site.register(Events)
# admin.site.register(Gallery)

@admin.register(Events)
class EventsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'organizer', 'start_time', 'tags')
    search_fields = ('name', 'organizer', 'venue',  'tags')
    list_filter = ('tags','start_time', 'prize', 'registration_fee', 'max_team_size', 'registration_deadline')
    list_per_page = 20
    fieldsets = (
        ('Basic Information', {
            'fields': (
                ('id', 'name'),
                ('organizer', 'venue'),
                ('start_time', 'end_time'),
                ('tags', 'prize'),
                ('registration_fee', 'registration_deadline'),
                ( 'description'),
                ('max_team_size', 'min_team_size'),
                ('poster', 'video'),
            ),
        }),
    )
    empty_value_display = '-empty-'

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('name', 'file', 'tags', 'tags')
    search_fields = ('name',)
    list_filter = ('tags', 'type')
    list_per_page = 20
    empty_value_display = '-empty-'