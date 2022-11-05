from django.urls import path, include
from . import views
from .views import *


event_urls = [
    path("allevents", views.all_events, name="allevents"),
    path("id/<str:event_id>", Get_Event_By_Id.as_view(), name="get_event_by_id"),
    path(
        "tags/<str:event_tags>", Get_Event_By_Tags.as_view(), name="get_event_by_tags"
    ),
]
