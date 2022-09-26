from urllib import request
from django.shortcuts import render
from django.http.request import HttpRequest
import json
from django.http import JsonResponse
from .models import User
from django.views import View

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

            new_user.save()
            return JsonResponse({'message': 'User created successfully!'})

