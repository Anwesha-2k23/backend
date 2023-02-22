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
import datetime
import razorpay
from user.utility import Autherize
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


class TeamEventRegistration(APIView):
    @Autherize()
    def post(self,request, **kwargs):
        user = kwargs['user']
        try: # taking input params
            event_id = request.data['event_id']
            team_name = request.data['team_name']
            team_members = request.data['team_members']
        except:
            return JsonResponse({"message":"Invalid or incomplete from data"}, status=403)

        try:
            event = Events.objects.get(id = event_id)
        except:
            return JsonResponse({"message":"event does not exists"},status=404)

        if Team.objects.filter(event_id = event,leader_id=user).exists(): 
            return JsonResponse({"message":"you are already registered in this event"},status=403)
        
        if Team.objects.filter(event_id = event,team_name=team_name).exists(): 
            return JsonResponse({"message":"A team with same name have already registered for this event"},status=403)
        
        if len(team_members)+1 > event.max_team_size or len(team_members)+1 < event.min_team_size:
            return JsonResponse({"message":"team size is not valid"},status=403)

        team_id = createId(prefix="TM",length=5)
        while Team.objects.filter(team_id = team_id).exists():
            team_id = createId(prefix="TM",length=5)

        # itrate over all team members and check id exists and not registered for this event
        error_msg = []
        for team_member in team_members:
            if not User.objects.filter(anwesha_id = team_member).exists():
                error_msg.append(team_member+" does not exists")
            elif TeamParticipant.objects.filter(anwesha_id = team_member, event_id = event).exists():
                error_msg.append(team_member+" is already registered in this event")
        
        if len(error_msg) > 0:
            return JsonResponse({"message":error_msg},status=403)
        
        # create payment object
        client = razorpay.Client(
            auth = (RAZORPAY_API_KEY_ID , RAZORPAY_API_KEY_SECRET)
        )
        event_fee = event.registration_fee
        print(event_fee)
        payment = client.order.create({
            "amount": int(event_fee),
            "currency": "INR",
        })
        
        try:
            new_team = Team(
                team_id = team_id,
                event_id = event,
                leader_id = user,
                team_name = team_name
            )
            new_team.save()
        except Exception as e:
            print(e)
            return JsonResponse({"message":"internal server error [team creation]"},status=500)
        
        try:
            new_payer = Payer.objects.create(
                payer_id = user,
                order_id = payment["id"],
                datetime = datetime.datetime.now()
            )
            new_payer.save()
        except Exception as e:
            print (e)


        for team_member in team_members:
            try:
                new_team_member = TeamParticipant(
                    team_id = new_team,
                    anwesha_id = User.objects.get(anwesha_id = team_member),
                    event_id = event,
                )
                new_team_member.save()
            except Exception as e:
                print(e)
                return JsonResponse({"message":"internal server error [teammate creation]"},status=500)

        return JsonResponse({ 
            "message":"Registered Partially", 
            "payment_details":payment,
            "team_id":team_id,
            "error": error_msg
            },status=201)

        
class SoloRegistration(APIView):
    @Autherize()
    def post(self,request, **kwargs):
        
        user = kwargs['user']
        try:
            event_id = request.data['event_id']
            event = Events.objects.get(id = event_id)
        except:
            return JsonResponse({"messagge":"this event does not exists please provide correct event id"},status=404)

        if SoloParicipants.objects.filter(event_id=event,anwesha_id=user.anwesha_id).exists():
            return JsonResponse({"messagge":"you have already registred for the events"},status=404)
        
        # implement order creation here
        client = razorpay.Client(
            auth = (RAZORPAY_API_KEY_ID , RAZORPAY_API_KEY_SECRET)
        )
        event_fee = event.registration_fee
        payment = client.order.create({
            "amount": int(event_fee),
            "currency": "INR",
        })

        try:
            this_person = SoloParicipants.objects.create(
                anwesha_id = user,
                event_id = event,
            )
            this_person.save()
        except:
            return JsonResponse({"message":"internal server error"},status=500)
        
        try:
            new_payer = Payer.objects.create(
                payer_id = user,
                order_id = payment["id"],
                datetime = datetime.datetime.now()
            )
            new_payer.save()
        except Exception as e:
            print (e)
        
        return JsonResponse({"message":"Event registration suceessfully completed","payment_details":payment},status=201)


class RazorpayCheckout(APIView):
    Autherize()
    def post(self,request, **kwargs):
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
            event_id = request.data['event_id']
        except:
            return JsonResponse({"message":"Incomplete or Invalid form data"},status=400)

        user = kwargs['user']
        try:
            team = Team.objects.get(leader_id = user, event_id = event_id)
        except:
            return JsonResponse({"message":"you are not the leader of this team"},status=403)
        
        try:
            payer = Payer.objects.get(team_id = team)
        except:
            return JsonResponse({"message":"you have not created any order for this team"},status=403)
        
        if razorpay_order_id != payer.order_id:
            return JsonResponse({"message":"your order id is not valid"},status=403)
        
        client = razorpay.Client(
            auth = (RAZORPAY_API_KEY_ID , RAZORPAY_API_KEY_SECRET)
        )
        data = {
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_order_id': razorpay_order_id,
            'razorpay_signature': razorpay_signature
        }
        
        check = client.utility.verify_payment_signature(data)
        print(check)
        if check:
            return JsonResponse({"message":"your payment signature is not valid" , "error":check},status=403)
        
        # update status in Payer table and Team table
        payer.status = "PAID"
        payer.save()

        team.payment_done = True
        team.save()
        
        return JsonResponse({"message":"success"},status=201)
            