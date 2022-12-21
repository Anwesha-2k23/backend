from django.shortcuts import render
from django.views import View
from utility import hashpassword, createId, isemail
from CA.models import campus_ambassador
from django.http import JsonResponse
from rest_framework.views import APIView
from utility import generate_jwt_token
from time import mktime

from datetime import datetime ,timedelta ,timezone
import jwt
# Create your views here.


def all_campas_ambassodor(request):
    if request.method == 'GET':
        events = campus_ambassador.objects.all()
        events = list(events.values('anwesha','email_id','full_name','college_name' ,'validation'))
        return JsonResponse(events, safe=False , status = 200)
    return JsonResponse({'message': 'Invalid method', 'status': '405'} , status=405) 


class register(APIView):
    def post(self, request):
        try:
            phone_number=request.data['phone_number']
            email_id=request.data['email_id']
            full_name=request.data['full_name']
            college_name=request.data['college_name']
            try:
                refferal_code=request.data['refferal_code']
            except:
                pass
            password=request.data['password']
            hpassword = hashpassword(password)
            if(isemail(email_id) == False):
                return JsonResponse({'message': 'Please enter valid email address', 'status': '409'} , status = 409)
            if campus_ambassador.objects.filter(email_id=email_id).exists():
                return JsonResponse({'message': 'An Campus Ambassador With same Email already exists', 'status': '409'},status = 409)
            if campus_ambassador.objects.filter(phone_number=phone_number).exists():
                return JsonResponse({'message': 'An Campus Ambassador With same Phone Number already exists', 'status': '409'},status = 409)
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
                return JsonResponse({'message': 'Campus ambassador created successfully!' ,'status':'201'} ,status=201)
        except:
            return JsonResponse({'message': 'Campus ambassador registration failed', 'status': '400'},status=400)

class leaderBoardData(View):
    def get(self , request):
        try:
            leaderBoard = campus_ambassador.objects.all().order_by('score')
            leaderBoard = list(leaderBoard.values('score','full_name','email_id').reverse())
            return JsonResponse ({"leaderBoardData" : leaderBoard , "status" : "200"},status=200)
        except:
            return JsonResponse({'message': 'Invalid method' , 'status': '405'},status=405)

class sendVerificationEmail(APIView):
    def post(self,request):
        try:
            email = request.data["email_id"]
            print(email)
            if campus_ambassador.objects.filter(email_id = email).exists():
                try:
                    payload = {
                        "email":email ,
                        "exp": datetime.utcnow() + timedelta(days=1),
                        "iat": datetime.utcnow()
                    } 
                    token = jwt.encode( payload=payload, key="secret" , algorithm="HS256") # not working ?? 
                    return JsonResponse({"token": token},status=201)
                except:
                    return JsonResponse({"message":"Token cannot be generated"} , status=409)
            else:
                return JsonResponse({"message":"No such email exists"},status=409)
        except:
            return JsonResponse({"message":"bad request"},status=400 )


def verifyEmail(request , *arg , **kwarg):
    if request.method == 'GET':
        token = kwarg['pk']
        try:
            jwt_payload = jwt.decode(token,"secret",algorithms = 'HS256') # not working ?? 
        except:
            return JsonResponse({"message":"token expired"} , status=409)
        try:
            ca_to_verify = campus_ambassador.objects.get(email_id = jwt_payload.email)
            ca_to_verify.validation = True
            campus_ambassador.save()
        except:
            return JsonResponse({"message":"Invalid Token"} , status=401)

        return JsonResponse({"message" : "email verified succesfully" } , status=201)