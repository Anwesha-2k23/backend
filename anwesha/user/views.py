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

from rest_framework.views import APIView
from rest_framework.response import Response
import datetime
import jwt
from utility import hashpassword, createId, isemail, generate_qr

class Login(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            return JsonResponse({"message": "you are unauthenticated , Please Log in First"} , status=401)

        try:
            payload = jwt.decode(token, "ufdhufhufgefef", algorithms = 'HS256')
        except jwt.ExpiredSignatureError:
            return JsonResponse({"message":"Your token is expired please generate new one"},status=409) 

        try:
            user = User.objects.get(anwesha_id = payload["id"])
            if(user.is_email_verified == True):
                user.is_loggedin = True
                user.save()
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
            return JsonResponse({"message":"invalid token"},status=409)

    def post(self, request):
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

                token = jwt.encode(payload, "ufdhufhufgefef", algorithm = 'HS256')

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
                payload = jwt.decode(token, "ufdhufhufgefef", algorithms = 'HS256')
            except jwt.ExpiredSignatureError:
                raise AuthenticationError("Cookie Expired")
            user = User.objects.get(anwesha_id = payload["id"]) 
            user.is_loggedin = False
            user.save()
            response = Response()
            response.delete_cookie('jwt')
            response.data = {'message': 'Logout Successful' , "status" : "200"}
            return response

class register(APIView):
    def post(self, request):
        try:
            password = request.data['password']
            email_id = request.data['email_id']
            full_name = request.data['full_name']
            phone_number = request.data['phone_number']
            if(isemail(email_id)== False):
                return JsonResponse({"message":"enter valid email"},status=409)
            if User.objects.filter(email_id=email_id).exists():
                return JsonResponse({'message': 'An User With same Email already exists', 'status': '409'},status = 409)
            if User.objects.filter(phone_number=phone_number).exists():
                return JsonResponse({'message': 'An User  With same Phone Number already exists', 'status': '409'},status = 409)
        except:
            return JsonResponse({"message":"required form data not recived"},status=401)
        # try:    
        #     password = hashpassword(password)
        #     anwesha_id = createId("ANW", 7)
        #     # checking if the created id is not already present in the database
        #     check_exist = User.objects.filter(anwesha_id = anwesha_id)
        #     while check_exist:  # very unlikely to happen
        #         anwesha_id = createId("ANW", 7)
        #         check_exist = User.objects.filter(anwesha_id = anwesha_id)
        #         # code for sending email
        #     generate_qr(anwesha_id=anwesha_id)
        # except:
        #     return JsonResponse({"message":"server side error due to issue in anweshaid generation"} , status=500)
        # try:    
        #     new_user = User.objects.create(full_name=full_name, email_id=email_id, password=password, phone_number=phone_number, anwesha_id=anwesha_id)
        #     shutil.move(anwesha_id+".png","static/qrcode/")
        #     new_user.qr_code="static/qrcode/"+anwesha_id+".png"
        #     new_user.save()
        # except:
        #     return JsonResponse({'message': 'User was not able to be saved due to server side error' , "status" : "500"},status=500)
        new_user = User.objects.create(full_name=full_name, email_id=email_id, password=password, phone_number=phone_number)
        new_user.save()
        return JsonResponse({'message': 'User created successfully!' , "status" : "201"})


class editProfile(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            return JsonResponse({"message": "you are unauthenticated , Please Log in First"} , status=401)

        try:
            payload = jwt.decode(token, "ufdhufhufgefef", algorithms = 'HS256')
        except jwt.ExpiredSignatureError:
            return JsonResponse({"message":"Your token is expired please generate new one"},status=409) 

        user = User.objects.get(anwesha_id = payload["id"]) 
        response = Response()
        response.data = {
            "anwesha_id": user.anwesha_id ,
            "full_name" : user.full_name ,
            "phone_number" : user.phone_number,
            "email_id" : user.email_id , 
            "college_name" : user.collage_name ,
            "age" : user.age , 
            "is_email_verified" : user.is_email_verified , 
            "gender" : user.gender ,
            "is_profile_completed" : user.is_profile_completed ,
        }
        return response
    def post(self, request):
        token = request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationError("Unauthenticated")

        try:
            payload = jwt.decode(token, "ufdhufhufgefef", algorithms = 'HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Cookie Expired")

        user = User.objects.get(anwesha_id = payload['id']) 
        data  =request.data
        try:
            full_name = data['full_name']
        except:
            full_name = user.full_name
        
        try:
            college_name = data['college_name']
        except:
            college_name = user.collage_name

        try:
            age = data['age']
        except:
            age = user.age

        try:
            gender = data['gender']
            if(gender == 'male'):
                gender = User.Gender.MALE
            if(gender == 'female'):
                gender = User.Gender.FEMALE
            if(gender == 'rather_not_say'):
                gender = User.Gender.RATHER_NOT_SAY
        except:
            gender = user.gender
                
        try:
            instagram_id = data['instagram_id']
        except:
            instagram_id = user.instagram_id

        try:
            facebook_id = data['facebook_id']
        except:
            facebook_id = user.facebook_id
        
        try:
            profile_photo = data['profile_photo']
        except:
            profile_photo = user.profile_photo

        user.full_name = full_name
        user.collage_name = college_name
        user.instagram_id = instagram_id
        user.facebook_id = facebook_id
        user.profile_photo = profile_photo
        user.age = age
        user.gender = gender
        user.save()
        response = Response()
        response.data = {
            'message': 'Profile successfully updated!'
        }
        return response

class sendVerificationEmail(APIView):
    def post(self,request):
        try:
            email = request.data["email_id"]
            if User.objects.filter(email_id = email).exists():
                try:
                    payload = {
                        "email":email ,
                        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
                        "iat": datetime.datetime.utcnow()
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
            jwt_payload = jwt.decode(token,"secret",algorithms = 'HS256')
        except:
            return JsonResponse({"message":"token expired"} , status=409)
        try:
            user_to_verify = User.objects.get(email_id = jwt_payload['email'])
            user_to_verify.is_email_verified = True
            user_to_verify.save()
        except:
            return JsonResponse({"message":"Invalid Token"} , status=401)
        return JsonResponse({"message" : "email verified succesfully" } , status=201)

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

def oauth(request):
    # print(request.user.username)
    # print(request.user.__dict__)
    print(dir(request.user.socialaccount_set.all))
    # print(request.user.first_name)
    print(request.user.email)

    return JsonResponse({'user':request.user},safe=False)