from django.urls import path, include
from . import views
from .views import *


event_urls = [
    path("allevents", views.all_events, name="allevents"),
    path("id/<str:event_id>", Get_Event_By_Id.as_view(), name="get_event_by_id"),
    path(
        "tags/<str:event_tags>", Get_Event_By_Tags.as_view(), name="get_event_by_tags"
    ),
    path("add_merch", add_merchandise.as_view(), name="add_merch"),
    path("order_merch", order_merchandise.as_view(), name="order_merch"),
    path("createteam",create_team.as_view() , name="create team"),
    path("team_member_registration",team_event_registration.as_view(),name="team registration"),
    path("solo_registration" ,solo_registration.as_view(),name="Solo event registration")
]
