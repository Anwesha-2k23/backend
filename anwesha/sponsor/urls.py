from django.urls import path
from .views import allsponsors

sponsor_urls = [
    path("allsponsors", allsponsors, name="alluser"),
    # path("register", register.as_view(), name="register"),
]
