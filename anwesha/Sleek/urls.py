from django.urls import path
from .views  import register

sleek_urls = [
    path('register', register, name='register'),    
]
