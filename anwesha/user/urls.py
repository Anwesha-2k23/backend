from django.urls import path, include
from .views  import LogOut,  Login, editProfile, register , ForgetPassword, verifyEmail , sendVerificationEmail,Oauth_Login, Oauth_Logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views

user_urls = [
    # path('alluser', alluser, name='alluser'),
    path('login', Login.as_view(), name='Login'),
    path('logout', LogOut.as_view() , name='logout'),
    path('editprofile' , editProfile.as_view() , name = 'editProfile'),
    path('register', register.as_view(), name='register'),
    path('forgetpassword', ForgetPassword.as_view() ,  name='forget_password_user'), # an upredicated 
    path('verifyemail' , sendVerificationEmail.as_view(), name='send_verificaion_email'),
    path('verifyemail/<str:pk>' , verifyEmail , name='verifyEmail' ),
    path('oauth-login/',Oauth_Login.as_view(),name='oauth-login'),
    path('oauth-logout/',Oauth_Logout.as_view(),name='oauth-logout'),
]
