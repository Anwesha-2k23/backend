from django.urls import path
# from . import views
from .views  import participant_register, team_register

participant_urls = [
    path('register', participant_register.as_view(), name='register'),
    path('team_register', team_register.as_view(), name='team_register'),
    path('myevents/',myevents,name='myevents')
]