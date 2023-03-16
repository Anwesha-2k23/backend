from django.http import JsonResponse
from django.views.generic import View
from rest_framework.views import APIView
from .models import Team,TeamParticipant,SoloParicipants,Payer, PayUTxn, Events,tag_dict
from utility import createId
from user.models import User
from anwesha.settings import COOKIE_ENCRYPTION_SECRET,RAZORPAY_API_KEY_ID , RAZORPAY_API_KEY_SECRET
import datetime
import razorpay
from user.utility import Autherize
from urllib.parse import unquote
from django.db.models import Q
# Create your views here.

# FBV for fetching all events
def all_events(request):
    if request.method == "GET":
        # events = Events.objects.all().order_by('order')
        events = Events.objects.filter(~Q(tags = 6)).order_by('order')
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
            
            # remove some fields
            del event['payment_link']
            del event['payment_key']

        return JsonResponse(events, safe=False)
    return JsonResponse({"message": "Invalid method" , "status": '405'},status=405)

class MyEvents(View):
    @Autherize()
    def get(self, request, **kwargs):
        user = kwargs['user']
        d2, d1 = [], []
        solo_participations = SoloParicipants.objects.filter(anwesha_id=user)
        for i in solo_participations:
            d1.append({
                'event_id': i.event_id.id,
                'event_name': i.event_id.name,
                'event_start_time': i.event_id.start_time,
                'event_end_time': i.event_id.end_time,
                'event_venue': i.event_id.venue,
                'event_tags': i.event_id.tags,
                'event_is_active': i.event_id.is_active,
                'order_id': i.order_id,
                'payment_done': i.payment_done,
                'payment_url' : i.event_id.payment_link
            })
        team_participations = TeamParticipant.objects.filter(anwesha_id=user)
        for i in team_participations:
            team_members = TeamParticipant.objects.filter(team_id=i.team_id)
            team_memberids = []
            for j in team_members:
                team_memberids.append(j.anwesha_id.anwesha_id)

            d2.append({
                'event_id': i.event_id.id,
                'event_name': i.event_id.name,
                'event_start_time': i.event_id.start_time,
                'event_end_time': i.event_id.end_time,
                'event_venue': i.event_id.venue,
                'event_tags': i.event_id.tags,
                'event_is_active': i.event_id.is_active,
                'order_id': i.team_id.txnid,
                'payment_done': i.team_id.payment_done,
                'team_name': i.team_id.team_name,
                'team_id': i.team_id.team_id,
                'team_lead': i.team_id.leader_id.full_name,
                'team_members': team_memberids,
                'payment_url' : i.event_id.payment_link
            })
        return JsonResponse({'solo': d1, 'team': d2}, safe=False)
        


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


class Check_Event_Registration(APIView):
    def post(self, request):
        try:
            signature = request.data['signature']
            print(signature)
            event_id = request.data['event_id']
            try:
                user = User.objects.get(signature=signature)
            except:
                return JsonResponse({"message": "Invalid signature"},status=400)
            try:
                event = Events.objects.get(id=event_id)
            except:
                return JsonResponse({"message": "Invalid event id"},status=403)
            if event.max_team_size == 1 and event.min_team_size == 1:
                if SoloParicipants.objects.filter(event_id=event_id, anwesha_id=user.anwesha_id, payment_done = True).exists():
                    soloparticipant = SoloParicipants.objects.get(event_id=event_id, anwesha_id=user.anwesha_id, payment_done = True)
                    return JsonResponse({"anwesha_id":user.anwesha_id,"username":user.full_name,"message": "User is Registered","has_entered":False},status=200)
                else:
                    return JsonResponse({"anwesha_id":user.anwesha_id,"username":user.full_name,"message": "User is not Registered"},status=401)
            else:
                if Team.objects.filter(event_id=event_id,leader_id=user.anwesha_id, payment_done = True).exists():
                    teamparticipant = TeamParticipant.objects.get(event_id=event_id,leader_id=user.anwesha_id, payment_done = True)
                    return JsonResponse({"anwesha_id":user.anwesha_id,"username":user.full_name,"message": "Team is Registered","has_entered": False},status=200)
                else:
                    return JsonResponse({"anwesha_id":user.anwesha_id,"username":user.full_name,"message": "Team is not Registered"},status=401)
        except:
            return JsonResponse({"message": "Invalid method" , "status": '405'},status=405)
        
class UpdateEntryStatus(APIView):
    def post(self,request):
        try:
            anwesha_id = request.data['anwesha_id']
            event_id = request.data['event_id']
            has_entered = request.data['has_entered']
        except:
            return JsonResponse({"message": "Invalid data"},status=405)
        try:
            event = Events.objects.get(id=event_id)
        except:
            return JsonResponse({"message": "Invalid event id"},status=402)
        try:
            if event.max_team_size == 1 and event.min_team_size == 1:
                soloparticipants = SoloParicipants.objects.get(event_id=event_id,anwesha_id=anwesha_id)
                soloparticipants.has_entered = has_entered
                soloparticipants.save()
                return JsonResponse({"message": "Updated successfully","new_status":soloparticipants.has_entered},status=200)
            else:
                teamparticipants = TeamParticipant.objects.get(event_id=event_id,anwesha_id=anwesha_id)
                teamparticipants.has_entered = has_entered
                teamparticipants.save()
                return JsonResponse({"message": "Updated successfully","new_status":teamparticipants.has_entered},status=200)
        except:
            return JsonResponse({"message": "Update fail"},status=400)
            

# class Rzpay_order_merchandise(APIView):
#     def post(self, request):
#         client = razorpay.Client(auth = (RAZORPAY_API_KEY_ID , RAZORPAY_API_KEY_SECRET))
#         try:
#             name = request.data['name']
#             address = request.data['address']
#             merch_title = request.data['merch_title']
#             size = request.data['size']
#             quantity = request.data['quantity']
#             # if order_merch.objects.filter(email=email).exists():
#             #     return JsonResponse({"message": "You have already ordered this merchandise" , "status": '409'},status=409)
#             try:
#                 merch = add_merch.objects.filter(title=merch_title)
#                 merch = merch[0]
#                 total_price = merch[0].prices[quantity]
#             except:
#                 return JsonResponse({"message":"Merch not found"})
#             payment = client.order.create(data = {
#                 "amount": int(total_price),
#                 "currency": "INR",
#             })
#             new_merch_order = order_merch.objects.create(name=name, address=address, merch_title = merch[0].title, size=size, quantity=quantity)
#             new_merch_order.order_id = payment["id"]
#             new_merch_order.save()
#             return JsonResponse({"message": "Merch is ordered successfully" , "status": '200'},status=200)
#         except:
#             response = JsonResponse({"message": "Merch not ordered" , "status": '405'},status=405)
#             return response

# class OrderMerchandise(APIView):
#     @Autherize()
#     def post(self,request, **kwargs):
#         user = kwargs['user']
#         try:
#             address = request.data['address']
#             merch_title = request.data['merch_title']
#             size = request.data['size']
#             quantity = request.data['quantity']
#             merch = add_merch.objects.get(title = merch_title)
#         except:
#             return JsonResponse({"messagge":"Merch does not exist"},status=404)

#         try:
#             new_merch = order_merch.objects.filter(merch_title=merch_title,anwesha_id=user.anwesha_id,address=address,size=size,quantity=quantity)
#             if new_merch[0].payment_done == True:
#                 return JsonResponse({"messagge":"You have already purchased this merch", "payment_details": new_merch[0].order_id },status=404)
            
#             return JsonResponse({"messagge":"you have already purchased this merch", "payment_details": new_merch[0].order_id, "payment_url": merch.payment_link },status=404)
#         except Exception as e:
#             print(e)
#             pass
        
#         # try:
#         new_merch = order_merch.objects.create(merch_title=merch, anwesha_id=user, address = request.data['address'], size = request.data['size'], quantity = request.data['quantity'])
#         new_merch.save()
#         # except:
#         #     return JsonResponse({"message":"internal server error"},status=500)
        
#         return JsonResponse({"message":"Merchandise purchase successful","payment_url": merch.payment_link},status=201)

class RzPayTeamEventRegistration(APIView):
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

  
class RzPaySoloRegistration(APIView):
    @Autherize()
    def post(self,request, **kwargs):
        
        client = razorpay.Client(
            auth = (RAZORPAY_API_KEY_ID , RAZORPAY_API_KEY_SECRET)
        )
        user = kwargs['user']
        try:
            event_id = request.data['event_id']
            event = Events.objects.get(id = event_id)
        except:
            return JsonResponse({"messagge":"this event does not exists please provide correct event id"},status=404)

        try:
            preRegister = SoloParicipants.objects.filter(event_id=event,anwesha_id=user.anwesha_id)
            order_id = preRegister[0].order_id
            order = client.order.fetch(order_id)
            if preRegister[0].payment_done == True:
                return JsonResponse({"messagge":"you have already registred for the events", "payment_details":order },status=404)
            
            event_fee = event.registration_fee
            payment = client.order.create(data = {
                "amount": int(event_fee),
                "currency": "INR",
            })
            preRegister[0].order_id = payment["id"]
            preRegister[0].save()
            return JsonResponse({"messagge":"you have already registred for the events", "payment_details":payment["id"] },status=404)
        except Exception as e:
            print(e)
            pass
        
        # implement order creation here
        event_fee = event.registration_fee
        payment = client.order.create(data = {
            "amount": int(event_fee),
            "currency": "INR",
        })

        try:
            this_person = SoloParicipants.objects.create(
                anwesha_id = user,
                event_id = event,
                order_id = payment["id"],
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
    @Autherize()
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
        except:
            return JsonResponse({"message":"Incomplete or Invalid form data"},status=400)

        user = kwargs['user']
        client = razorpay.Client(
            auth = (RAZORPAY_API_KEY_ID , RAZORPAY_API_KEY_SECRET)
        )
        data = {
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_order_id': razorpay_order_id,
            'razorpay_signature': razorpay_signature
        }
        
        try:
            client.utility.verify_payment_signature(data)
        except:
            return JsonResponse({"message":"Invalid signeture"},status=403)

        try:
            solo_participant = SoloParicipants.objects.get(order_id = razorpay_order_id)
            solo_participant.payment_done = True
            solo_participant.save()
        except:
            pass

        try:
            payer = Payer.objects.get(order_id = razorpay_order_id)
            payer.payment_status = Payer.Payment_Status.PAID
            payer.payment_id = razorpay_payment_id
            payer.signature = razorpay_signature
            payer.datetime = datetime.datetime.now()
            payer.save()
            if payer.team_id:
                payer.team_id.payment_done = True
                payer.team_id.save()
        except Exception as e:
            print(e)
            return JsonResponse({"message":"Signeture varrified", "error": "payment entry not found" },status=403)
        
        return JsonResponse({"message":"Signeture varified" },status=200)
        
        
def webhook(request):
    request_data = {
        "method" : request.method,
        "body" : request.body,
        "get" : request.GET,
    }
    with open("sus1.txt", "a") as f:
        f.write(str(request_data))
        f.write(",\n")
        f.close()

    db = unquote(request.body.decode("utf-8")).split("&")
    bdy = {}
    for d in db:
        _d = d.split("=")
        bdy[_d[0]] = None
        if len(_d) == 2:
            bdy[_d[0]] = _d[1]

    if PayUTxn.objects.filter(txnid=bdy["txnid"]).exists():
        return JsonResponse({"message":"repeated request"},status=200)
    
    try:
        payUclient = PayUTxn.objects.create(
            txnid = bdy["txnid"],
            mihpayid = bdy["mihpayid"],
            mode = bdy["mode"],
            key = bdy["key"],
            amount = bdy["amount"],
            addedon = bdy["addedon"],
            productinfo = bdy["productinfo"],
            firstname = bdy["firstname"],
            email = bdy["email"],
            phone = bdy["phone"],
            status = bdy["status"],
            field1 = bdy["field1"],
            field2 = bdy["field2"],
            field3 = bdy["field3"],
            field4 = bdy["field4"],
            field5 = bdy["field5"],
        )
        payUclient.save()
    except Exception as e:
        print(e)
        pass
    
    merch_payments = [
        "24493298", "24498465", "24498352"
    ]

    if bdy["productinfo"].split("+")[-1] in merch_payments:
        return JsonResponse({"message":"webhook recieved"},status=200)

    try:
        if bdy["status"] != "success":
            return JsonResponse({"message":"webhook Failed"},status=200)
        event = Events.objects.get(payment_key = bdy["productinfo"])
        user = User.objects.get(email_id = bdy["email"])
        try:
            soloreg = SoloRegistration.objects.get(event_id = event, anwesha_id = user)
            soloreg.payment_done = True
            soloreg.order_id = bdy["txnid"]
            soloreg.save()
            return JsonResponse({"message":"webhook recieved"},status=200)
        except :
            pass

        try:
            teamreg = Team.objects.get(event_id = event, leader_id = user)
            teamreg.payment_done = True
            teamreg.txnid = bdy["txnid"]
            teamreg.save()
            return JsonResponse({"message":"webhook recieved"},status=200)
        except :
            pass
    except:
        return JsonResponse({"message":"webhook Failed"},status=500)    
    return JsonResponse({"message":"webhook recieved"},status=200)

class SoloRegistration(APIView):
    @Autherize()
    def post(self,request, **kwargs):
        user = kwargs['user']
        print(user.user_type == User.User_type_choice.IITP_STUDENT)
        try:
            event_id = request.data['event_id']
            event = Events.objects.get(id = event_id)
        except:
            return JsonResponse({"messagge":"this event does not exists please provide correct event id"},status=404)

        try:
            preRegister = SoloParicipants.objects.filter(event_id=event,anwesha_id=user.anwesha_id)
            if preRegister[0].payment_done == True:
                print("flag")
                return JsonResponse({"messagge":"you have already registred for the events", "payment_details": preRegister[0].order_id },status=200)
            
            return JsonResponse({"messagge":"you have already registred for the events", "payment_details": preRegister[0].order_id, "payment_url": event.payment_link },status=200)
        except Exception as e:
            print(e)
            pass
        
        # implement order creation here

        try:
            this_person = SoloParicipants.objects.create(
                anwesha_id = user,
                event_id = event,
            )
            if user.user_type == User.User_type_choice.IITP_STUDENT and event.tags != '5':  
                this_person.payment_done = True
                this_person.save()
                return JsonResponse({"message":"Event registration suceessfully completed", "payment_url": None },status=201)
            this_person.save()
        except:
            return JsonResponse({"message":"internal server error"},status=500)
        
        return JsonResponse({"message":"Event registration suceessfully completed","payment_url": event.payment_link},status=201)


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

        if len(Team.objects.filter(event_id = event,leader_id=user,payment_done = True )) >= 1: 
            return JsonResponse({"message":"you are already registered in this event"},status=403)
        
        if len(Team.objects.filter(event_id = event,leader_id=user,payment_done = False )) >= 1: 
            return JsonResponse({"message":"you are already registered in this event, but payment not varified yet", "payment_url": event.payment_link },status=403)
        
        if len(Team.objects.filter(event_id = event,team_name=team_name)) >= 1: 
            return JsonResponse({"message":"A team with same name have already registered for this event"},status=403)
        
        if len(team_members) > event.max_team_size or len(team_members) < event.min_team_size:
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

        if user.user_type == User.User_type_choice.IITP_STUDENT:
            new_team.payment_done = True
            new_team.save()
            return JsonResponse(
                {"message":"Registered Successfully", 
                 "team_id":team_id,
                "error": error_msg,
                "payment_url": None}
                ,status=201)

        return JsonResponse({ 
            "message":"Registered Partially", 
            "payment_url": event.payment_link,
            "team_id":team_id,
            "error": error_msg
            },status=201)
