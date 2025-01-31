from django.contrib import admin
from .models import Payments

@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('anwesha_id', 'event_id', 'event_type', 'email_id', 'atompay_transaction_id', 'bank_transaction_id')
    search_fields = ('anwesha_id__username', 'event_id__name', 'email_id', 'atompay_transaction_id', 'bank_transaction_id')
    list_filter = ('event_type',)
