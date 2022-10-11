from django.urls import path
# from . import views
from .views  import participant_register

participant_urls = [
    path('register', participant_register.as_view(), name='register'),
]
