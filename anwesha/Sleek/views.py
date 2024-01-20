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
        if request.method == 'POST':

         data = request.body
         payload = json.loads(data)

          #CREATE TOKEN HERE 
         print(token)

        if not token:
         return JsonResponse({"message": "you are unauthenticated , Please Log in First"} , status=401)
        try:
            user = User.objects.get(anwesha_id = payload["id"])
            if(user.is_email_verified == True):
                user.is_loggedin = True                
                response  = []; 
                response.append('Welcome Your AnweshaID is' + user.anwesha_id)
                return JsonResponse({"message":respose , 'status':200 })
            else:
                return JsonResponse({"message":"Your Email is not verified please verify email to continue further"},status=401)
        except: 
            print("Registring")
            stime = time.time()
          
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

