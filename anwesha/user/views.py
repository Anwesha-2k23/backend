import shutil
from urllib import request
from django.shortcuts import render
from django.http.request import HttpRequest
import json
from multiprocessing import AuthenticationError
from urllib import response
from django.shortcuts import render
from django.http import JsonResponse
from .models import User
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.hashers import make_password, check_password

# from .serializers import UserSerializers
from rest_framework.views import APIView
from rest_framework.response import Response
import datetime
import jwt
from utility import hashpassword, createId, isemail, generate_qr

# def alluser(request):
#     if request.method == 'GET':
#         users = User.objects.all()
#         users = list(users.values())
#         return JsonResponse(users, safe=False)
#     else:
#         response = JsonResponse({'message': 'Hello, World!'})
#         return response

class Login(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            # print("no token")
            raise AuthenticationError("Unauthenticated")

        try:
            payload = jwt.decode(token, "ufdhufhufgefef", algorithms = 'HS256')
        except jwt.ExpiredSignatureError:
            # print("expired")
            raise AuthenticationError("Cookie Expired")

        user = User.objects.get(anwesha_id = payload["id"]) 
        response = Response()
        response.data = {
            "mssg": "welcome",
            "full_name" : user.full_name
        }
        return response

    def post(self, request):
        response = Response()
        try:
            username = request.data['username']
            password = request.data['password']
        except:
            response.data = { "status" : "Incorrrect input" }
            return response

        password = hashpassword(password)
        # print(password)
        user = None
        if isemail(username):
            user = User.objects.filter(email_id = username, password = password)
        else:
            user = User.objects.filter(anwesha_id = username , password=password)
        
        if user:
            this_user = user[0]

            payload = {
                "id" : this_user.anwesha_id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                "iat": datetime.datetime.utcnow()
            }

            token = jwt.encode(payload, "ufdhufhufgefef", algorithm = 'HS256')
            
            response.data = { "success" : True , "name" : this_user.full_name}
            response.set_cookie(key='jwt', value=token, httponly=True)

            # code for linking cookie
        else:
            response.data = { "successs": False, "message": "incorrect id or password" }

        return response    


class LogOut(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationError("Unauthenticated")
        else:
            response = Response()
            response.delete_cookie('jwt')
            response.data = {'message': 'Logout Successful'}
            return response



class register(APIView):
    def post(self, request):
        password = request.data['password']
        email_id = request.data['email_id']
        full_name = request.data['full_name']

        # print(password)
        password = hashpassword(password)
        anwesha_id = createId("ANW", 7)

        generate_qr(anwesha_id=anwesha_id)

        # checking if the created id is not already present in the database
        check_exist = User.objects.filter(anwesha_id = anwesha_id)
        while check_exist:  # very unlikely to happen
            anwesha_id = createId("ANW", 7)
            check_exist = User.objects.filter(anwesha_id = anwesha_id)

        # code for sending email

        new_user = User.objects.create(full_name=full_name, email_id=email_id, password=password, anwesha_id=anwesha_id)
        new_user.qr_code="static/qrcode/"+anwesha_id+".png"
        shutil.move(anwesha_id+".png","static/qrcode/")
        new_user.save()
        return JsonResponse({'message': 'User created successfully!'})


class editProfile(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationError("Unauthenticated")

        try:
            payload = jwt.decode(token, "ufdhufhufgefef", algorithms = 'HS256')
        except jwt.ExpiredSignatureError:
            print("expired")
            raise AuthenticationError("Cookie Expired")

        user = User.objects.get(anwesha_id = payload["id"]) 
        response = Response()
        response.data = {
            "anwesha_id": user.anwesha_id ,
            "full_name" : user.full_name ,
            "phone_number" : user.phone_number,
            "email_id" : user.email_id , 
            "college_name" : user.college_name ,
            # "profile_photo" : user.profile_photo , 
            "age" : user.age , 
            "is_email_verified" : user.is_email_verified , 
            "user_type" : user.user_type ,
            "gender" : user.gender ,
            "is_profile_completed" : user.is_profile_completed ,
        }
        return response

    def post(self ,request):
       token = request.COOKIES.get('jwt')
       if not token:
           raise AuthenticationError("Unauthenticated")      
       try:
           payload = jwt.decode(token, "ufdhufhufgefef", algorithm = 'HS256')
       except jwt.ExpiredSignatureError:
           raise AuthenticationError("Cookie Expired")      
       user = User.objects.get(anwesha_id = payload["id"]) 
       user.phone_number = request.data['phone_number']
       user.full_name  = request.data['full_name ']
       user.college_name = request.data['college_name']
       user.age = request.data['age']
       user.user_type  = request.data['user_type ']
       user. instagram_id = request.data['instagram_id']
       user.facebook_id  = request.data['facebook_id']
       user.save()
       response = Response()
       response.data = user
       user.save()
       return response

class forgetPassword(APIView):
    def post(self,request):
        email_id = request.data['email_id']
        email_user = User.objects.get(email_id = email_id)
        if email_user:
            pass
        else:
            response = Response()
            response.data = { "successs": False, "message": "This email doesnt exist for any user" }
            return response

class forgetPassword2(APIView):
    def get(self,post):
        pass