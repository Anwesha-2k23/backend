from django.contrib import admin
from .models import FestPasses

@admin.register(FestPasses)
class FestPassesAdmin(admin.ModelAdmin):
    list_display = ('anwesha_id', 'email_id', 'transaction_id', 'has_entered', 'payment_done')
    list_filter = ('has_entered', 'payment_done')
    search_fields = ('anwesha_id__anwesha_id', 'email_id', 'transaction_id')
    ordering = ('anwesha_id',)

    def get_readonly_fields(self, request, obj=None):
        if obj:  
            return ('anwesha_id', 'transaction_id', 'email_id')
        return ()  
