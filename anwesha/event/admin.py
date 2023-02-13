from django.contrib import admin
from .models import Events, Gallery, add_merch, order_merch
from utility import export_as_csv
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
    actions = [export_as_csv]

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('name', 'file', 'tags', 'tags')
    search_fields = ('name',)
    list_filter = ('tags', 'type')
    list_per_page = 20
    empty_value_display = '-empty-'

@admin.register(add_merch)
class add_merchAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'prices', 'size', 'image')
    search_fields = ('title',)
    empty_value_display = '-empty-'
    actions = [export_as_csv]

@admin.register(order_merch)
class order_merchAdmin(admin.ModelAdmin):
    def merch(self, obj):
        return obj.merch_title.title

    list_display = ('name', 'email', 'phone_no', 'address','size','quantity','payment_status','merch')
    search_fields = ['name','email','phone_no','merch_title__title']
    empty_value_display = '-empty-'
    actions = [export_as_csv]