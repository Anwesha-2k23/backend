from django.urls import path
from .views import register

multicity_urls = [
    path('register' , register.as_view(), name='register'),
]