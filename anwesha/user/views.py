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
from anwesha.settings import AWS_S3_CUSTOM_DOMAIN, COOKIE_ENCRYPTION_SECRET
import jwt
from utility import hashpassword, createId, isemail, generate_qr, EmailSending, hash_id
import time
from .utility import Autherize , send_email_using_microservice , mail_content
import threading
from anwesha.settings import  AWS_PUBLIC_MEDIA_LOCATION2
from django.shortcuts import redirect

class Login(APIView):
    def get(self, request):
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
                user.save()
                response = Response()
                response.data = {
                    "mssg": "welcome",
                    "full_name" : user.full_name,
                    "anwesha_id" : user.anwesha_id,
                    "user_type" : user.user_type,
                    "status" : "200"
                }
                return response
            else:
                return JsonResponse({"message":"Your Email is not verified please verify email to continue further"},status=403)
        except:
            return JsonResponse({"message":"invalid token"},status=409)

    def post(self, request):
        response = Response()
        try:
            username = request.data['username']
            password = request.data['password']
        except:
            response.data = { "status" : "Incorrrect input" }
            response.status = 404
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
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=1440),
                    "iat": datetime.datetime.utcnow()
                }

                token = jwt.encode(payload, COOKIE_ENCRYPTION_SECRET, algorithm = 'HS256')
                this_user.is_loggedin = True
                response.data = { 
                    "success" : True , 
                    "name" : this_user.full_name ,
                    "anwesha_id" : this_user.anwesha_id,
                    "user_type" : this_user.user_type,
                    }
                response.set_cookie(key='jwt', value=token, httponly=True,samesite=None)
                return response
            else:
                return JsonResponse({"message":"Please verify email to log in to your account"},status=403)
            # code for linking cookie
        else:
            return JsonResponse({"message":"Incorrect Credentials"},status=401)
    def options(self, request):
        return "200"    


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

class register(APIView):
    def post(self, request):
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
        new_user = User.objects.create(
            full_name=full_name,
            email_id=email_id, 
            password=password, 
            phone_number=phone_number,
            is_email_verified = True,
            user_type=user_type,
            collage_name=college_name,
        )
        new_user.save()

        # e = EmailSending(new_user)
        # threading.Thread(target=e.email_varification).start()
        # t = time.time()
        text = mail_content(type = 1,email_id = email_id , full_name = full_name , anwesha_id = new_user.anwesha_id)
        send_email_using_microservice(
            email_id=email_id,
            subject="No reply",
            text=text
        )
        # print(time.time() - t)
        return JsonResponse({'message': 'User created successfully!' , "status" : "201"})


class editProfile(APIView):
    @Autherize()
    def get(self, request, **kwargs):
        user = kwargs['user']
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
            "profile_pitcure":str(user.profile_photo),
            "user_type": user.user_type,
            "qr_code":'https://'+ AWS_S3_CUSTOM_DOMAIN +'/'+ AWS_PUBLIC_MEDIA_LOCATION2 +  str(user.qr_code)
        }
        return response
    
    @Autherize()
    def post(self, request, **kwargs):
        user = kwargs['user']
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
                        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=10),
                        "iat": datetime.datetime.utcnow()
                    } 
                    token = jwt.encode( payload=payload, key=COOKIE_ENCRYPTION_SECRET , algorithm="HS256") # not working ?? 
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
            jwt_payload = jwt.decode(token,COOKIE_ENCRYPTION_SECRET,algorithms = 'HS256')
        except:
            return JsonResponse({"message":"token expired"} , status=409)
        try:
            user_to_verify = User.objects.get(anwesha_id = jwt_payload['id'])
            user_to_verify.is_email_verified = True
            user_to_verify.save()
        except:
            return JsonResponse({"message":"Invalid Token"} , status=401)
        #return JsonResponse({"message" : "email verified succesfully" } , status=201)
        return redirect('https://anwesha.live/userLogin')
    
class ForgetPassword(APIView):
    def get():  # for clicking the sent link
        pass

    def post(self, request):  # posting the email address // mail the link
        if not request.data['email']:
            return Response({"message": "Email is missing"}, status=400)
        try:
            user = User.objects.get(email_id=request.data['email'])
            payload = {
                'userid': user.anwesha_id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=7200),
                "iat": datetime.datetime.utcnow()
            }

            token = jwt.encode(
                payload, COOKIE_ENCRYPTION_SECRET, algorithm='HS256')
            link = "http://anwesha.live/user/reset_password/"+token
            text = f'''Hello {user.full_name}!\nThis is the link to change password click it to update your password:-\n{link}\nPS: please dont share it with anyone\nThanks\nTeam Anwesha'''
            ## send mail
            send_email_using_microservice(email_id=request.data['email'],subject="Change password",text=text)
            return Response({"message": "Reset Link sent"}, status=200)
        except:
            return Response({"message": "Email not found"}, status=404)

    def put(self, request):  # chanfing the password
        token = request.data['token']
        password = request.data['password']

        try:
            payload = jwt.decode(token, COOKIE_ENCRYPTION_SECRET, 'HS256')
        except jwt.ExpiredSignatureError:
            return Response({"message": "Cookie Expired"}, status=408)

        try:
            user = User.objects.get(anwesha_id=payload['userid'])
        except:
            return Response({"message": "Invalid cookie"}, status=404)

        user.password = hashpassword(password)
        user.save()

        # send mail confirmation
        return Response({"message": "Password updated"}, status=200)
    
class RegenerateQR(APIView):
    @Autherize()
    def get(self, request, **kwargs):
        user = kwargs['user']
        user.secret = createId("secret",10)
        user.signature = hash_id(user.anwesha_id, user.secret)
        user.qr_code = generate_qr(user.signature)
        user.save()
        return JsonResponse({
            "qr_code":'https://'+ AWS_S3_CUSTOM_DOMAIN +'/'+ str(user.qr_code)
        },safe=False)

class Oauth_Login(APIView):
    def get(self,request):
        username = request.user.username
        first_name = request.user.first_name
        email = request.user.email
        last_name = request.user.last_name
        full_name = first_name + last_name

        #registering user in custom user model
        if User.objects.filter(email_id=email).exists():
            user = User.objects.get(email_id=email) 
            payload = {
                        "id" : user.anwesha_id,
                        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=1440),
                        "iat": datetime.datetime.utcnow()
                    }
            response = Response()
            token = jwt.encode(payload, COOKIE_ENCRYPTION_SECRET, algorithm = 'HS256')
            response.set_cookie(key='jwt', value=token, httponly=True)
            user.is_loggedin=True
            user.save()
            response.data={'user':'logged in','username':username,'first_name':first_name, 'last_name':last_name,'email':email}
            return response
        else:
            anwesha_id = createId("ANW", 7)
            password = uuid.uuid1()
            anwesha_id_hash = hash_id(anwesha_id)
            generate_qr(anwesha_id=anwesha_id_hash)
            # checking if the created id is not already present in the database
            check_exist = User.objects.filter(anwesha_id = anwesha_id)
            while check_exist:  # very unlikely to happen
                anwesha_id = createId("ANW", 7)
                check_exist = User.objects.filter(anwesha_id = anwesha_id)
            new_user = User.objects.create(full_name=full_name, password = password, email_id=email, anwesha_id=anwesha_id)
            new_user.qr_code="static/qrcode/"+anwesha_id+".png"
            shutil.move(anwesha_id+".png","static/qrcode/")
            new_user.is_loggedin=False
            new_user.save()
            user = User.objects.get(email_id=email) 
            payload = {
                        "id" : user.anwesha_id,
                        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                        "iat": datetime.datetime.utcnow()
                    }
            response = Response()
            token = jwt.encode(payload, COOKIE_ENCRYPTION_SECRET, algorithm = 'HS256')
            response.set_cookie(key='jwt', value=token, httponly=True)
            user.is_loggedin=True
            user.save()
            response.data={'user':'registered','username':username,'first_name':first_name, 'last_name':last_name,'email':email}
            return response
            
    # return JsonResponse({'status':'success' },safe=False)

class Oauth_Logout(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt')
            
        if not token:
            raise AuthenticationError("Unauthenticated")

        try:
            payload = jwt.decode(token, COOKIE_ENCRYPTION_SECRET, algorithms = 'HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Cookie Expired")

        user = User.objects.get(anwesha_id = payload['id']) 
        user.is_loggedin=False
        user.save()
        response = Response()
        response.delete_cookie('jwt')
        return response