from django.shortcuts import render
import json
from django.http import JsonResponse
from .models import User
# Create your views here.

# def alluser(request):
#     if request.method == 'GET':
#         users = User.objects.all()
#         users = list(users.values())
#         return JsonResponse(users, safe=False)
#     else:
#         response = JsonResponse({'message': 'Hello, World!'})
#         return response

