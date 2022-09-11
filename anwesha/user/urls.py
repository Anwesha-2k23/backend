from django.urls import path, include
from .views  import alluser, Login , logout
from django.views.decorators.csrf import csrf_exempt


user_urls = [
    path('alluser', alluser, name='alluser'),
    path('login', Login.as_view(), name='Login'),
    path('logout', logout , name='logout'),
]