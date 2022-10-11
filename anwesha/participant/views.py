from django.shortcuts import render
from .models import Participant, Leader, Payer
from user.models import User
from event.models import Events
from django.views import View
from django.http import JsonResponse

# Create your views here.
class participant_register(View):
    def post(self, request):
        try:
            event_id = request.POST.get('event_id')
            anwesha_id = request.POST.get('anwesha_id')
            new_user = User.objects.get(anwesha_id=anwesha_id)
            new_event = Events.objects.get(id=event_id)
            
            participant = Participant.objects.create(anwesha_id=new_user, event_id=new_event)
            participant.save()

            return JsonResponse({'message': 'Participant registered successfully'})
        except:
            return JsonResponse({'message': 'An Error occured'})