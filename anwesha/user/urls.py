from django.urls import path, include
from . import views



user_urls = [
    # path('alluser', views.alluser, name='alluser'),
    # path('register.as_view()', views.register, name='register'),
    path('register', views.register.as_view(), name='register'),

]