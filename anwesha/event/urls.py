from django.urls import path, include
from . import views
from .views import *


event_urls = [
    path("allevents", views.all_events, name="allevents"),
    path("id/<str:event_id>", Get_Event_By_Id.as_view(), name="get_event_by_id"),
    path(
        "tags/<str:event_tags>", Get_Event_By_Tags.as_view(), name="get_event_by_tags"
    ),
    path("order_merch", OrderMerchandise.as_view(), name="order_merch"),
    # path("createteam",create_team.as_view() , name="create team"),
    path("registration/team",TeamEventRegistration.as_view(),name="team registration"),
    path("registration/solo" ,SoloRegistration.as_view(),name="Solo event registration"),
    path("registration/verification" , RazorpayCheckout.as_view(), name = "Check payment"),
    path("myevents", MyEvents.as_view(), name="myevents"),
    path("payment/webhook/very/sus/api", views.webhook, name="webhook"),
]
