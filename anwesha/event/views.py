from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
import json
from .models import Events, tag_dict, add_merch, order_merch
from rest_framework.views import APIView
from .models import Team,TeamParticipant,SoloParicipants,Payer
from utility import createId
from user.models import User
from anwesha.settings import COOKIE_ENCRYPTION_SECRET,RAZORPAY_API_KEY_ID , RAZORPAY_API_KEY_SECRET
import jwt
import razorpay
# Create your views here.

# FBV for fetching all events
def all_events(request):
    if request.method == "GET":
        events = Events.objects.all()
        events = list(events.values())
        for event in events:
            k = event['organizer']
            k = k.split(',')
            m = []
            for i in k:
                m.append(i.split(":"))
            event['organizer'] = m
            event['is_solo'] = False
            if event['max_team_size'] == 1 and event['min_team_size'] == 1: event['is_solo'] = True

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
            team = Team.objects.create(
                team_id = team_id,
                event_id=event,
                leader_id=leader_id,
                team_name=team_name
            )
            team.save()
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
            team_participant = TeamParticipant.objects.create(
                anwesha_id = team_member,
                event_id = event,
                team_id = team
            )
            team_participant.save()
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
            this_person = SoloParicipants.objects.create(
                anwesha_id = user,
                event_id = event,
            )
            this_person.save()
        except:
            return JsonResponse({"message":"internal server error"},status=500)
        
        # implement order creation here
        
        client = razorpay.Client(
            auth = (RAZORPAY_API_KEY_ID , RAZORPAY_API_KEY_SECRET)
        )
        event_fee = event.registration_fee
        payment = client.order.create({
            "amount":event_fee,
            "currency": "INR",
        })
        return JsonResponse({"message":"Event registration suceessfully completed","payment_details":payment},status=201)

        
# class RazorpayCheck(APIView):
#     def post(self,request):
#         token = request.COOKIES.get('jwt')

#         if not token:
#             return JsonResponse({"message": "you are unauthenticated , Please Log in First"} , status=401)

#         try:
#             payload = jwt.decode(token,COOKIE_ENCRYPTION_SECRET , algorithms = 'HS256')
#         except jwt.ExpiredSignatureError:
#             return JsonResponse({"message":"Your token is expired please login again"},status=409) 
#         total_price = request.data['total_price']

#         payment = client.order.create({
#             "amount":total_price,
#             "currency": "INR",
#         })
#         return JsonResponse({"message":"Payment order created","payment_details":payment},status=200)

class RazorpayCheckout(APIView):
    def post(self,request):
        """
        payment type is a string 
        valid payment types are
        :solo-event: -> for payment of solo event 
        :team-event: -> for payment of team events
        """
        try:
            razorpay_payment_id = request.data['razorpay_payment_id']
            razorpay_order_id = request.data['razorpay_order_id']
            razorpay_signature = request.data['razorpay_signature']
            payment_type:request.data['payment_type']
            event_id = request.data['event_id']
        except:
            return JsonResponse({"message":"Incomplete or Invalid form data"},status=400)

        # token verification step
        token = request.COOKIES.get('jwt')
        if not token:
            return JsonResponse({"message": "you are unauthenticated , Please Log in First"} , status=401)
        try:
            payload = jwt.decode(token,COOKIE_ENCRYPTION_SECRET , algorithms = 'HS256')
        except jwt.ExpiredSignatureError:
            return JsonResponse({"message":"Your token is expired please login again"},status=409)

        if payment_type == "solo-event":
            payer_id  = User.objects.get(anwesha_id = payer_id['id'])
            team_id = None
        elif payment_type == "team-event":
            payer_id  = User.objects.get(anwesha_id = payer_id['id'])
            
            if Team.objects.filter(leader_id = payload['id'], event_id=event_id).exists():
                team = Team.objects.get(leader_id = payload['id'], event_id=event_id)
                team_id = team
            else:
                return JsonResponse({"message":"you are not allowed to perform this action , payment for a event is done only by the team leaders"},status=403)

        else:
            return JsonResponse({"message":"Incomplete or Invalid form data"},status=400)


        client = razorpay.Client(
            auth = (RAZORPAY_API_KEY_ID , RAZORPAY_API_KEY_SECRET)
        )
        data = {}
        data['razorpay_payment_id'] = razorpay_payment_id
        data['razorpay_order_id'] = razorpay_order_id
        data['razorpay_signature'] = razorpay_signature

        check = client.utility.verify_payment_signature(data)

        if check:
            return JsonResponse({"message":"your payment signature is not valid" , "error":check},status=403)
        
        Payer.objects.create(
            team_id = team,
            payer_id = payer_id,
            payment_status = Payer.Payment_Status.PAID,
            payment_id = razorpay_payment_id,
            order_id = razorpay_order_id,
            signature = razorpay_signature
        )
        Payer.save()

        if payment_type == "solo-event":
            participant = SoloParicipants.objects.get(anwesha_id = payer_id)
            participant.payment_done = True
            participant.save()

        if payment_type == "team-event":
            team = Team.objects.get(team_id = team_id)
            team.payment_done = True
            team.save()
        
        return JsonResponse({"message":"success"},status=201)
            