from django.urls import path, include
from . import views



event_urls = [
    path('allevents', views.all_events, name='allevents'),
]