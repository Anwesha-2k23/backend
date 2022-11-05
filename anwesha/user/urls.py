from django.urls import path, include
from .views import LogOut, alluser, Login, editProfile, register
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views

user_urls = [
    path("alluser", alluser, name="alluser"),
    path("login", Login.as_view(), name="Login"),
    path("logout", LogOut.as_view(), name="logout"),
    path("editprofile", editProfile.as_view(), name="editProfile"),
    path("register", register.as_view(), name="register"),
]
