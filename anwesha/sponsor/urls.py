from django.urls import path
from .views import allsponsors

sponsor_urls = [
    path("allsponsors", allsponsors, name="alluser"),
]
