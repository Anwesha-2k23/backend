from django.urls import path, include
from .views  import LogOut,  Login, editProfile, register , forgetPassword, verifyEmail , sendVerificationEmail,Oauth_Login, Oauth_Logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views

user_urls = [
    # path('alluser', alluser, name='alluser'),
    path('register', register, name='register')

    
]
