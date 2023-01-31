from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
import json
from .models import Events, tag_dict, add_merch, order_merch
from rest_framework.views import APIView

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