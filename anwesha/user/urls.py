from django.urls import path, include
from . import views
from .views  import register, Login , logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views

user_urls = [
    path('login', Login.as_view(), name='Login'),
    path('logout', logout , name='logout'),
    path('reset_password', auth_views.PasswordResetView.as_view() , name= "reset_password"), # to chance template in this use template_name = <template path> in as_view function
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view() , name = "password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view() , name="password_reset_confirm"),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view() , name="password_reset_complete"),
    path('register', register.as_view(), name='register'),
]

# password reset reference video = https://www.youtube.com/watch?v=sFPcd6myZrY
