from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import Events
from django.views.generic import View

# Create your views here.

#FBV for getting all events
def all_events(request):
    if request.method == 'GET':
        events = Events.objects.all()
        events = list(events.values())
        return JsonResponse(events, safe=False)
    else:
        response = JsonResponse({'message': 'An Error occured'})
        return response

#CBV for getting event details from event id
class Event_from_id(View):
    def get(self,request,event_id):
        event = Events.objects.get(id=event_id).__dict__
        event.pop('_state')
        return JsonResponse(event, safe=False)
