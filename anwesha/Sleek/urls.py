from django.urls import path, include
from .views  import LogOut,  Login, editProfile, register , forgetPassword, verifyEmail , sendVerificationEmail,Oauth_Login, Oauth_Logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views

user_urls = [
    # path('alluser', alluser, name='alluser'),
    path('Register', Login.as_view(), name='register'),
    path('login', Login.as_view(), name='login'),
    path('logout', LogOut.as_view() , name='logout'),

    
]
