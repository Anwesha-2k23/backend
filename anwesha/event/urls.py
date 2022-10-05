from django.urls import path, include
from . import views
from .views import *


event_urls = [
    path('allevents', views.all_events, name='allevents'),
    path('<str:event_id>', Event_from_id.as_view(), name='event'),
]