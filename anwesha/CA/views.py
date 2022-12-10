from django.shortcuts import render
from django.views import View
from utility import hashpassword, createId, isemail
from CA.models import campus_ambassador
from django.http import JsonResponse
from rest_framework.views import APIView
# Create your views here.


def all_campas_ambassodor(request):
    if request.method == 'GET':
        events = campus_ambassador.objects.all()
        events = list(events.values('anwesha','email_id','full_name','college_name'))
        return JsonResponse(events, safe=False)
    return JsonResponse({'message': 'Invalid method', 'status': '405'}) 


class register(APIView):
    def post(self, request):
        try:
            phone_number=request.data['phone_number']
            email_id=request.data['email_id']
            full_name=request.data['full_name']
            college_name=request.data['college_name']
            refferal_code=request.data['refferal_code']
            password=request.data['password']
            print("refferal code = ",phone_number)
            hpassword = hashpassword(password)
            if(isemail(email_id) == False):
                return JsonResponse({'message': 'Please enter valid email address', 'status': '409'})
            if campus_ambassador.objects.filter(email_id=email_id).exists():
                return JsonResponse({'message': 'An Campus Ambassador With same Email already exists', 'status': '409'})
            else:
                new_campus_ambassador = campus_ambassador.objects.create(
                    full_name=full_name,
                    email_id=email_id, 
                    password=hpassword, 
                    phone_number = phone_number , 
                    college_name = college_name , 
                    refferal_code = refferal_code , 
                    )
                new_campus_ambassador.save()
                return JsonResponse({'message': 'Campus ambassador created successfully!' , 'status': '201'})
        except:
            return JsonResponse({'message': 'Campus ambassador registration failed', 'status': '400'})

class leaderBoardData(View):
    def get(self , request):
        try:
            leaderBoard = campus_ambassador.objects.all().order_by('score')
            leaderBoard = list(leaderBoard.values('score','full_name','email_id').reverse())
            return JsonResponse ({"leaderBoardData" : leaderBoard , "status" : "200"})
        except:
            return JsonResponse({'message': 'Invalid method' , 'status': '405'})