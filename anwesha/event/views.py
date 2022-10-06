from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
import json
from .models import Events

# Create your views here.

#FBV for fetching all events
def all_events(request):
    if request.method == 'GET':
        events = Events.objects.all()
        events = list(events.values())
        return JsonResponse(events, safe=False)
    return JsonResponse({'message': 'An Error occured'}) 

#CBV for fetching event by id
class Get_Event_By_Id(View):
    def get(self, request, event_id):
        try:
            event = Events.objects.get(id=event_id)
            event = event.__dict__
            event.pop('_state')
            return JsonResponse(event, safe=False)
        except:
            response = JsonResponse({'message': 'An Error occured'})
            return response
