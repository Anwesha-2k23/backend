from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
import json
from .models import Events, tag_dict, add_merch, order_merch
from rest_framework.views import APIView
from participant.models import Team,TeamParticipant,SoloParicipants
from utility import createId
from user.models import User
from anwesha.settings import COOKIE_ENCRYPTION_SECRET
import jwt
# Create your views here.

# FBV for fetching all events
def all_events(request):
    if request.method == "GET":
        events = Events.objects.all()
        events = list(events.values())
        return JsonResponse(events, safe=False)
    return JsonResponse({"message": "Invalid method" , "status": '405'},status=405)


# CBV for fetching event by id
class Get_Event_By_Id(View):
    def get(self, request, event_id):
        try:
            event = Events.objects.get(id=event_id)
            event = event.__dict__
            event.pop("_state")
            return JsonResponse(event, safe=False,status=200)
        except:
            response = JsonResponse({"message": "Invalid method" , "status": '405'},status=405)
            return response


class Get_Event_By_Tags(View):
    def get(self, request, event_tags):
        try:
            events = Events.objects.filter(tags=tag_dict[event_tags])
            events = list(events.values())
            return JsonResponse(events, safe=False)
        except:
            response = JsonResponse({"message": "Invalid method" , "status": '405'},status=405)
            return response

class add_merchandise(APIView):
    def post(self, request):
        try:
            title = request.data['title']
            description = request.data['description']
            prices = request.data['prices']
            size = request.data['size']
            image = request.data['image']
            if add_merch.objects.filter(title=title).exists():
                return JsonResponse({"message": "Merch already exists with this title" , "status": '409'},status=409)

            new_merch = add_merch.objects.create(title=title, description=description, prices=prices, size=size, image=image)
            new_merch.save()
            return JsonResponse({"message": "Merch is added successfully" , "status": '200'},status=200)
        except:
            response = JsonResponse({"message": "Merch not added" , "status": '405'},status=405)
            return response

class order_merchandise(APIView):
    def post(self, request):
        try:
            name = request.data['name']
            email = request.data['email']
            phone_no = request.data['phone_no']
            address = request.data['address']
            merch_title = request.data['merch_title']
            size = request.data['size']
            quantity = request.data['quantity']
            if order_merch.objects.filter(email=email).exists():
                return JsonResponse({"message": "You have already ordered this merchandise" , "status": '409'},status=409)

            new_order = order_merch.objects.create(name=name, email=email, phone_no=phone_no, address=address, merch_title = add_merch.objects.get(title = merch_title), size=size, quantity=quantity)
            new_order.save()
            return JsonResponse({"message": "Merch is ordered successfully" , "status": '200'},status=200)
        except:
            response = JsonResponse({"message": "Merch not ordered" , "status": '405'},status=405)
            return response

class create_team(APIView):
    def post(sef,request):
        token = request.COOKIES.get('jwt')

        if not token:
            return JsonResponse({"message": "you are unauthenticated , Please Log in First"} , status=401)

        try:
            payload = jwt.decode(token,COOKIE_ENCRYPTION_SECRET , algorithms = 'HS256')
        except jwt.ExpiredSignatureError:
            return JsonResponse({"message":"Your token is expired please login again"},status=409) 

        try:
            event_id = request.data['event_id']
            team_name = request.data['team_name']
        except:
            return JsonResponse({"message":"Invalid or incomplete from data"}, status=403)

        team_id = createId(prefix="TM",length=5)
        check_exist = Team.objects.filter(team_id = team_id).exists()
        while check_exist:
            team_id = createId(prefix="TM",length=5)
            check_exist = Team.objects.filter(team_id = team_id).exists()


        try:
            event = Events.objects.get(id = event_id)
        except:
            return JsonResponse({"messagge":"this event does not exists please provide correct event id"},status=404)

        if Team.objects.filter(event_id = event,team_name=team_name).exists():
            return JsonResponse({"message":"A team with same name have already registered for this event"},status=403)

        if Team.objects.filter(leader_id = payload['id']):
            return JsonResponse({"message":"you are already registered in this event"},status=403)

        try:
            leader_id = User.objects.get(anwesha_id = payload["id"])
        except:
            return JsonResponse({"message": "Anwesha ID does not exist"},status=400)

        if not leader_id.is_email_verified:
            return JsonResponse({"message":"Your Email is not verified please verify email to continue further"},status=401)
        
        try:
            Team.objects.create(
                team_id = team_id,
                event_id=event,
                leader_id=leader_id,
                team_name=team_name
            )
        except:
            return JsonResponse({"message":"internal server error"},status=500)

        return JsonResponse({"message":"Team sucessfully created","team id":team_id},status=201)
class team_event_registration(APIView):
    def post(self,request):
        token = request.COOKIES.get('jwt')

        if not token:
            return JsonResponse({"message": "you are unauthenticated , Please Log in First"} , status=401)

        try:
            payload = jwt.decode(token,COOKIE_ENCRYPTION_SECRET , algorithms = 'HS256')
        except jwt.ExpiredSignatureError:
            return JsonResponse({"message":"Your token is expired please login again"},status=409) 
        try:
            event_id = request.data['event_id']
            team_id = request.data['team_id']
            team_member_id = request.data['team_member']
        except:
            return JsonResponse({"message":"Invalid or incomplete from data"}, status=403)

        if not User.objects.filter(anwesha_id = payload['id']).exists():
            return JsonResponse({"message":"this user does not exist"},status=404)

        try:
            team = Team.objects.get(team_id=team_id)
        except:
            return JsonResponse({"message":"Wrong team id provided"},status=400)

        if not str(team.leader_id) == payload['id']: 
            return JsonResponse({"message":"you are not authenticated for this operation only team leaders are allowed to perform this operation"},status=403)



        if not User.objects.filter(anwesha_id = team_member_id).exists():
            return JsonResponse({"message": "provided anwesha id does not exists" },status=404) 

        team_member = User.objects.get(anwesha_id = team_member_id)

        try:
            event = Events.objects.get(id = event_id)
        except:
            return JsonResponse({"messagge":"this event does not exists please provide correct event id"},status=404)

        if TeamParticipant.objects.filter(event_id=event_id, anwesha_id = team_member.anwesha_id).exists():
            return JsonResponse({"messagge":"Memeber already exists"},status=403)

        try:
            TeamParticipant.objects.create(
                anwesha_id = team_member,
                event_id = event,
                team_id = team
            )
        except:
            return JsonResponse({"message":"internal server error"},status=500)
        return JsonResponse({"message":"Team member suceessffully added"},status=201)

        
class solo_registration(APIView):
    def post(self,request):
        token = request.COOKIES.get('jwt')

        if not token:
            return JsonResponse({"message": "you are unauthenticated , Please Log in First"} , status=401)

        try:
            payload = jwt.decode(token,COOKIE_ENCRYPTION_SECRET , algorithms = 'HS256')
        except jwt.ExpiredSignatureError:
            return JsonResponse({"message":"Your token is expired please login again"},status=409) 
        try:
            event_id = request.data['event_id']
        except:
            return JsonResponse({"message":"Invalid or incomplete from data"}, status=403)

        try:
            user = User.objects.get(anwesha_id = payload['id'])
        except:
            return JsonResponse({"message":"this user does not exist"},status=404)

        try:
            event = Events.objects.get(id = event_id)
        except:
            return JsonResponse({"messagge":"this event does not exists please provide correct event id"},status=404)

        if SoloParicipants.objects.filter(event_id=event,anwesha_id=payload["id"]).exists():
            return JsonResponse({"messagge":"you have already registred for the events"},status=404)
        try:
            SoloParicipants.objects.create(
                anwesha_id = user,
                event_id = event,
            )
        except:
            return JsonResponse({"message":"internal server error"},status=500)
        return JsonResponse({"message":"Event registration suceessfully completed"},status=201)

        