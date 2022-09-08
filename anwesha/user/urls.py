from django.urls import path, include
from . import views



user_urls = [
    path('alluser', views.alluser, name='alluser'),
]