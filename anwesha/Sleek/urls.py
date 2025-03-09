from django.urls import path, include
from .views import register
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views

sleek_urls = [
    # path('alluser', alluser, name='alluser'),
    path('register', register, name='register')
]
