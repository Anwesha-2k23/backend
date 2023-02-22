from django.contrib import admin
from .models import Events, Gallery, add_merch, order_merch
from .models import TeamParticipant, Team, Payer,SoloParicipants
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
    readonly_fields = ['id']
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




@admin.register(TeamParticipant)
class ParticipantAdmin(admin.ModelAdmin):

    @admin.action(description='Lock Selected User')
    def lock_user(self, request, queryset):
        queryset.update(is_locked=True)
        self.message_user(request, "Selected User Locked")

    list_display = ('anwesha_id', 'event_id', 'team_id')
    search_fields = ('anwesha_id', 'event_id', 'team_id')
    actions = [lock_user,export_as_csv]

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):

    @admin.action(description='Lock Selected User')
    def lock_user(self, request, queryset):
        queryset.update(is_locked=True)
        self.message_user(request, "Selected User Locked")

    list_display = ('team_id', 'event_id', 'leader_id', 'team_name')
    search_fields = ('team_id', 'event_id', 'leader_id', 'team_name')
    actions = [lock_user,export_as_csv]
@admin.register(Payer)
class PayerAdmin(admin.ModelAdmin):

    @admin.action(description='Lock Selected User')
    def lock_user(self, request, queryset):
        queryset.update(is_locked=True)
        self.message_user(request, "Selected User Locked")

    list_display = ('team_id', 'payer_id', 'payment_status',)
    search_fields = ('team_id', 'payer_id', 'reference_id')
    list_filter = ('payment_status',)
    actions = [lock_user,export_as_csv]   
@admin.register(SoloParicipants)
class SoloAdmin(admin.ModelAdmin):

    @admin.action(description='Lock Selected User')
    def lock_user(self, request, queryset):
        queryset.update(is_locked=True)
        self.message_user(request, "Selected User Locked")

    list_display = ('anwesha_id', 'event_id', 'payment_done')
    search_fields = ('anwesha_id', 'event_id')
    list_filter = ('payment_done',)
    actions = [lock_user,export_as_csv]