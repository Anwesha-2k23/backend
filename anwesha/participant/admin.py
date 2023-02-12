from django.contrib import admin

from .models import TeamParticipant, Team, Payer,SoloParicipants

# Register your models here.
# admin.site.register(Participant)
# admin.site.register(Team)
# admin.site.register(Payer)


@admin.register(TeamParticipant)
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
    
@admin.register(SoloParicipants)
class SoloAdmin(admin.ModelAdmin):
    list_display = ('anwesha_id', 'event_id', 'payment_done')
    search_fields = ('anwesha_id', 'event_id')
    list_filter = ('payment_done',)