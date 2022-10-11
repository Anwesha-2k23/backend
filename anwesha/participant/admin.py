from django.contrib import admin

from .models import Participant, Leader, Payer

# Register your models here.
admin.site.register(Participant)
admin.site.register(Leader)
admin.site.register(Payer)