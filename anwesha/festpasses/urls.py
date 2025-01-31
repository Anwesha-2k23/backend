from django.urls import path
from .views import *

festpasses_urls = [
    path('atompay',payview,name="payview"),
    path('response',resp,name="response"),
    path('register',festpasses.as_view(),name="festpasses"),
    path('getStatus',getStatus.as_view(),name = "getStatus"),
    path('setStatus',setStatus.as_view(),name="setStatus")
]