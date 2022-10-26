from django.shortcuts import render
from .models import Participant, Leader, Payer
from user.models import User
from event.models import Events
from django.views import View
from django.http import JsonResponse
from utility import get_anwesha_id

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

#FBV to get all events in which current user is registered
def myevents(request):
    if request.method == "GET":
        try:
            anwesha_id = get_anwesha_id(request=request)
            if anwesha_id is None:
                return JsonResponse({'message': 'Unauthenticated'})
            else:
                my_events_list = Participant.objects.filter(anwesha_id = anwesha_id)
                my_events_list = list(my_events_list.values())
                return JsonResponse(my_events_list,safe=False)
        except:
            return JsonResponse({'message': 'An Error occured'})