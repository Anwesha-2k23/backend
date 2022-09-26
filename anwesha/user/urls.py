<<<<<<< HEAD
from django.urls import path, include
from . import views



user_urls = [
    # path('alluser', views.alluser, name='alluser'),
    # path('register.as_view()', views.register, name='register'),
    path('register', views.register.as_view(), name='register'),

]
=======
from django.urls import path, include
from .views  import alluser, Login , logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views

user_urls = [
    path('alluser', alluser, name='alluser'),
    path('login', Login.as_view(), name='Login'),
    path('logout', logout , name='logout'),
    path('reset_password', auth_views.PasswordResetView.as_view() , name= "reset_password"), # to chance template in this use template_name = <template path> in as_view function
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view() , name = "password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view() , name="password_reset_confirm"),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view() , name="password_reset_complete"),
]

# password reset reference video = https://www.youtube.com/watch?v=sFPcd6myZrY
>>>>>>> 0d912ee54515a4eadde6ce5388d29331ef72098f
