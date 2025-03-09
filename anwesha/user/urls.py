from django.urls import path, include
from .views  import EditProfile, Register , ForgetPassword, verifyEmail , SendVerificationEmail, RegenerateQR,Login ,LogOut,AppLogin
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views

user_urls = [
    path('login', Login.as_view(), name='Login'),
    path('logout', LogOut.as_view() , name='logout'),
    path('login/app',AppLogin.as_view(),name="applogin"),
    path('editprofile' , EditProfile.as_view() , name = 'editProfile'),
    path('register', Register.as_view(), name='register'),
    path('forgetpassword', ForgetPassword.as_view() ,  name='forget_password_user'),
    path('verifyemail' , SendVerificationEmail.as_view(), name='send_verificaion_email'),
    path('verifyemail/<str:pk>' , verifyEmail , name='verifyEmail' ),
    path('regenerateqr/', RegenerateQR.as_view(), name='regenerateqr'),
]
