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
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
import datetime
from anwesha.settings import COOKIE_ENCRYPTION_SECRET
import jwt
from utility import hashpassword, createId, isemail, generate_qr


def register( request):
        token = request.COOKIES.get('jwt')
        if not token:
            return JsonResponse({"message": "you are unauthenticated , Please Log in First"} , status=401)

        try:
            payload = jwt.decode(token, COOKIE_ENCRYPTION_SECRET, algorithms = 'HS256')
        except jwt.ExpiredSignatureError:
            return JsonResponse({"message":"Your token is expired please generate new one"},status=409) 

        try:
            user = User.objects.get(anwesha_id = payload["id"])
            if(user.is_email_verified == True):
                user.is_loggedin = True
                response = Response()
                response.data = {
                    "mssg": "welcome",
                    "full_name" : user.full_name,
                    "status" : "200"
                }
                return response
            else:
                return JsonResponse({"message":"Your Email is not verified please verify email to continue further"},status=401)
        except: 
            print("Registring")
            stime = time.time()
        try:    
            password = request.data['password']
            email_id = request.data['email_id']
            full_name = request.data['full_name']
            phone_number = request.data['phone_number']
            college_name = request.data['college_name']
            user_type = request.data['user_type']
            """
             data validation
            """
            if(isemail(email_id)== False):
                return JsonResponse({"message":"enter valid email"},status=409)
            if User.objects.filter(email_id=email_id).exists():
                return JsonResponse({'message': 'An User With same Email already exists', 'status': '409'},status = 409)
            if User.objects.filter(phone_number=phone_number).exists():
                return JsonResponse({'message': 'An User  With same Phone Number already exists', 'status': '409'},status = 409)

            """
            assiging user types
            """
            if(user_type == "iitp_student"):
                user_type = User.User_type_choice.IITP_STUDENT
            elif user_type == "student":
                user_type = User.User_type_choice.STUDENT
            elif user_type == "non-student":
                user_type = User.User_type_choice.NON_STUDENT
            elif user_type == "non-student":
                user_type = User.User_type_choice.NON_STUDENT
            elif user_type == "alumni":
                user_type = User.User_type_choice.ALUMNI
            elif user_type == "faculty":
                user_type = User.User_type_choice.GUEST
            else:
                return JsonResponse({"message":"enter proper user type"},status=403)    

        except:
            return JsonResponse({"message":"required form data not recived"},status=401)
        itime = time.time()
        print(f"time after validation {itime-stime}")
        print(full_name,email_id,password,college_name,user_type)
        new_user = User.objects.create(
            full_name=full_name,
            email_id=email_id,
            password=password,
            phone_number=phone_number,
            is_email_verified = True,
            user_type=user_type,
            collage_name=college_name,
        )
        print("New user created successfully")
        print(new_user)
        new_user.save()
        Anwesha_id =[]

        Anwesha_id.append('Successfully Registered , Your AnsweshaID is' + new_user.anwesha_id); 

        # e = EmailSending(new_user)
        # threading.Thread(target=e.email_varification).start()
        # t = time.time()
        # text = mail_content(type = 1,email_id = email_id , full_name = full_name , anwesha_id = new_user.anwesha_id)
        #send_email_using_microservice(
            #email_id=email_id,
            #subject="No reply",
            #text=text
        #)
        # print(time.time() - t)
        return JsonResponse({'message': Anwesha_id , "status" : "201"})      

def login( request):
        response = Response()
        try:
            username = request.data['username']
            password = request.data['password']
        except:
            response.data = { "status" : "Incorrrect input" }
            return response

        password = hashpassword(password)
        user = None
        if isemail(username):
            user = User.objects.filter(email_id = username, password = password)
        else:
            user = User.objects.filter(anwesha_id = username , password=password)
        this_user = user.first()
        
        if user:
            if this_user.is_email_verified == True :
                payload = {
                    "id" : this_user.anwesha_id,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                    "iat": datetime.datetime.utcnow()
                }

                token = jwt.encode(payload, COOKIE_ENCRYPTION_SECRET, algorithm = 'HS256')

                response.data = { "success" : True , "name" : this_user.full_name}
                response.set_cookie(key='jwt', value=token, httponly=True)
            else:
                response.data = {
                    "message" : "Please verify email to log in to your account",
                    "success" : False
                }
            # code for linking cookie
        else:
            response.data = { "successs": False, "message": "incorrect id or password" }

        return response    


class LogOut(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationError("Unauthenticated")
        else:
            try:
                payload = jwt.decode(token, COOKIE_ENCRYPTION_SECRET, algorithms = 'HS256')
            except jwt.ExpiredSignatureError:
                raise AuthenticationError("Cookie Expired")
            user = User.objects.get(anwesha_id = payload["id"]) 
            user.is_loggedin = False
            user.save()
            response = Response()
            response.delete_cookie('jwt')
            response.data = {'message': 'Logout Successful' , "status" : "200"}
            return response




