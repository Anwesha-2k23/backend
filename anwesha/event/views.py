from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import Events

# Create your views here.

def all_events(request):
    if request.method == 'GET':
        events = Events.objects.all()
        events = list(events.values())
        return JsonResponse(events, safe=False)
    else:
        response = JsonResponse({'message': 'An Error occured'})
        return response