from django.contrib import admin

from .models import TeamParticipant, Team, Payer,SoloParicipants
from utility import export_as_csv

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