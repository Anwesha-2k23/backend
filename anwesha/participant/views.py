from tabnanny import check
from django.shortcuts import render
from .models import Participant, Team, Payer
from user.models import User
from event.models import Events
from django.views import View
from django.http import JsonResponse
from utility import createId
from utility import get_anwesha_id

# Create your views here.
class participant_register(View):
    def post(self, request):
        try:
            event_id = request.POST.get("event_id")
            anwesha_id = request.POST.get("anwesha_id")
            new_user = User.objects.get(anwesha_id=anwesha_id)
            new_event = Events.objects.get(id=event_id)

            participant = Participant.objects.create(
                anwesha_id=new_user, event_id=new_event
            )
            participant.save()

            return JsonResponse({"message": "Participant registered successfully" , "status": "201"},status=201)
        except:
            return JsonResponse({"message": "Participant registration failed" , "status": "400"},status=400)


class team_register(View):
    def post(self, request):
        try:
            event_id = request.POST.get("event_id")
            event_id = Events.objects.get(id=event_id)
            leader_id = request.POST.get("leader_id")
            leader_id = User.objects.get(anwesha_id=leader_id)

            team_id = createId("TEAM", 10)

            check_exist = Team.objects.filter(team_id=team_id)
            while check_exist:
                team_id = createId("TEAM", 10)
                check_exist = Team.objects.filter(team_id=team_id)

            new_team = Team.objects.create(
                team_id=team_id, event_id=event_id, leader_id=leader_id
            )
            new_team.save()
            return JsonResponse({"message": "Team created successfully" , "status": "201"},status=201)
        except:
            return JsonResponse({"message": "Team creation failed" , "status": "400"},status=400)


# FBV to get all events in which current user is registered
def myevents(request):
    if request.method == "GET":
        try:
            anwesha_id = get_anwesha_id(request=request)
            if anwesha_id is None:
                return JsonResponse({"message": "Unauthenticated" , "status": "401"},status=401)
            else:
                my_events_list = Participant.objects.filter(anwesha_id=anwesha_id)
                my_events_list = list(my_events_list.values())
                return JsonResponse(my_events_list, safe=False)
        except:
            return JsonResponse({"message": "Invalid method" , "status": "405"},status=405)
