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
from utility import hashpassword
import datetime
import jwt
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated

# class UserViewSet(viewsets.ModelViewSet):
#     permission_classes = IsAuthenticated
#     serializer_class = UserSerializers
#     queryset = User.objects.all()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# class Login(APIView):
#     def login(request):
#         print(request)  
#         if request.method == 'POST':
#             anwesha_id  = request.POST.get('anwesha_id')
#             password = request.POST.get('password')
#             user = User.objects.filter(anwesha_id =anwesha_id , password=password)
#             if user:
#                 this_user = list(User.objects.get(anwesha_id =anwesha_id , password=password))
#                 return JsonResponse(this_user)
#             else:
#                 return JsonResponse({'message': 'Invalid Anwesha ID or Password'})
#         else:
#             return JsonResponse({'message': 'Invalid Request'})

class Login(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationError("Unauthenticated")

        try:
            payload = jwt.decode(token, "ufdhufhufgefef", algorithm = 'HS256')
        except jwt.ExpiredSignatureError:
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
            anwesha_id = request.data['anwesha_id']
            password = request.data['password']
        except:
            response.data = { "status" : "Incorrrect input" }
            return response

        password = hashpassword(password)
        print(password)
        user = User.objects.filter(anwesha_id =anwesha_id , password=password)
        if user:
            this_user = user[0]

            payload = {
                "id" : anwesha_id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                "iat": datetime.datetime.utcnow()
            }

            token = jwt.encode(payload, "ufdhufhufgefef", algorithm = 'HS256').decode('utf-8')
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



# @csrf_exempt
# # @ensure_csrf_cookie
# def logout(request):
#         if request.method == 'POST':
#             request.session.clear()
#             return JsonResponse({'message': 'Logout Successful'})
#         else:
#             return JsonResponse({'message': 'Invalid Request'})

class register(View):
    def post(self, request):
        if request.method == 'POST':
            anwesha_id=request.POST.get('anwesha_id')
            password=request.POST.get('password')
            phone_number=request.POST.get('phone_number')
            email_id=request.POST.get('email_id')
            full_name=request.POST.get('full_name')
            college_name=request.POST.get('college_name')
            profile_photo=request.POST.get('profile_photo')
            age=request.POST.get('age')
            is_email_verified=request.POST.get('is_email_verified')
            user_type=request.POST.get('user_type')
            qr_code=request.POST.get('qr_code')
            gender=request.POST.get('gender')
            accomadation_selected=request.POST.get('accomadation_selected')
            is_profile_completed=request.POST.get('is_profile_completed')
            instagram_id=request.POST.get('instagram_id')
            facebook_id=request.POST.get('facebook_id')
            time_of_registration=request.POST.get('time_of_registration')

        
            new_user = User.objects.create(anwesha_id=anwesha_id, password=password, phone_number=phone_number, email_id=email_id, full_name=full_name, college_name=college_name, profile_photo=profile_photo, age=age, is_email_verified=is_email_verified, user_type=user_type, qr_code=qr_code, gender=gender, accomadation_selected=accomadation_selected, is_profile_completed=is_profile_completed, instagram_id=instagram_id, facebook_id=facebook_id, time_of_registration=time_of_registration)
            password = make_password(password)
            new_user.save()
            return JsonResponse({'message': 'User created successfully!'})
        else:
            return JsonResponse({'message': 'User not created!'})
