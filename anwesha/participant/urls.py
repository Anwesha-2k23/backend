from django.urls import path
# from . import views
from .views  import participant_register,myevents

participant_urls = [
    path('register', participant_register.as_view(), name='register'),
    path('myevents/',myevents,name='myevents')
]
