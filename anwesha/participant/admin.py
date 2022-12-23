from django.contrib import admin

from .models import Participant, Team, Payer

# Register your models here.
# admin.site.register(Participant)
# admin.site.register(Team)
# admin.site.register(Payer)


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('anwesha_id', 'event_id', 'team_id')
    search_fields = ('anwesha_id', 'event_id', 'team_id')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_id', 'event_id', 'leader_id', 'team_name')
    search_fields = ('team_id', 'event_id', 'leader_id', 'team_name')

@admin.register(Payer)
class PayerAdmin(admin.ModelAdmin):
    list_display = ('team_id', 'payer_id', 'payment_status',)
    search_fields = ('team_id', 'payer_id', 'reference_id')
    list_filter = ('payment_status',)
    